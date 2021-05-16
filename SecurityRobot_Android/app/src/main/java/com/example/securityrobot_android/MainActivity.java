package com.example.securityrobot_android;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.net.http.SslError;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.SslErrorHandler;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MainActivity extends AppCompatActivity {

    private String serverUrl = "tcp://175.27.245.39:1883";   //MQTT服务器 端口
    private String userName = "mosquitto";   //MQTT用户名
    private String passWord = "mosquitto";   //MQTT密码
    private String mqtt_sub_topic = "monitor";  //订阅的主题
    private String matt_pub_movetop = "move";
    private String clientId = "app"+System.currentTimeMillis();
    private MqttClient mqtt_client;                         //创建一个mqtt_client对象
    private WebView webView;
    MqttConnectOptions options;

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        makeToast("MQTT连接中...");
        mqtt_init_Connect();
        makeToast("MQTT连接成功");

        ImageView Img_facedetection = findViewById(R.id.image_FaceDetection);  //监听facedetection的动作
        ImageView videoReload = findViewById(R.id.VideoReload);  //监听刷新视频监控的动作

        Img_facedetection.setOnTouchListener(new View.OnTouchListener() {     //人脸事件页面跳转监测
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN){    //按下松开后运行
                    Intent intent=new Intent(MainActivity.this, MyWebview.class);  //页面刷新
                    startActivity(intent);
                }
                return true;
            }
        });

        videoReload.setOnTouchListener(new View.OnTouchListener() {    //向上事件监测
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN){    //按下松开后运行
                   webView.reload();
                }
                return true;
            }
        });

        video();
    }

    public void mqtt_init_Connect()  //初始化MQTT客户端，建立MQTT连接
    {
        try {
            TextView Tempvalue = findViewById(R.id.TempValue);
            TextView Humivalue = findViewById(R.id.HumiValue);
            TextView Smokevalue = findViewById(R.id.SmokeValue);
            TextView Firevalue = findViewById(R.id.fireValue);
            ImageView top = findViewById(R.id.image_top);
            ImageView down = findViewById(R.id.image_down);
            ImageView left = findViewById(R.id.image_left);
            ImageView right = findViewById(R.id.image_right);
            //实例化mqtt_client，填入我们定义的serverUri和clientId，然后MemoryPersistence设置clientid的保存形式，默认为以内存保存
            mqtt_client = new MqttClient(serverUrl,clientId,new MemoryPersistence());
            //创建并实例化一个MQTT的连接参数对象
            options = new MqttConnectOptions();
            //然后设置对应的参数
            options.setUserName(userName);                  //设置连接的用户名
            options.setPassword(passWord.toCharArray());    //设置连接的密码
            options.setConnectionTimeout(30);               // 设置超时时间，单位为秒
            options.setKeepAliveInterval(50);               //设置心跳,30s
            options.setAutomaticReconnect(true);            //是否重连
            //设置是否清空session,设置为false表示服务器会保留客户端的连接记录，设置为true表示每次连接到服务器都以新的身份连接
            options.setCleanSession(true);

            //设置回调
            mqtt_client.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable cause) {
                    //连接丢失后，一般在这里面进行重连
                    cause.printStackTrace();
                    System.out.println("connectionLost");
                }
                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {
                    //publish后会执行到这里
                    System.out.println("发送成功");
                }
                @Override
                public void messageArrived(String topicName, MqttMessage message) throws Exception {
                    //subscribe后得到的消息会执行到这里面
//                    System.out.println("接收消息主题 : " + topicName);
//                    System.out.println("接收消息Qos : " + message.getQos());
//                    System.out.println("接收消息内容 : " + new String(message.getPayload()));

                    String[] mess=new String(message.getPayload()).split("#");  //分割收到的数据

                    if(mess.length>=4) {
                        if (Integer.parseInt(mess[0]) == 0) {     // 有烟雾、燃气
                            Smokevalue.post(new Runnable() {
                                @Override
                                public void run() {
                                    Smokevalue.setText("有");
                                }
                            });
                        } else {
                            Smokevalue.post(new Runnable() {  // 无烟雾、燃气
                                @Override
                                public void run() {
                                    Smokevalue.setText("无");
                                }
                            });
                        }

                        if (Integer.parseInt(mess[4]) == 0) {     // 有火
                            Firevalue.post(new Runnable() {
                                @Override
                                public void run() {
                                    Firevalue.setText("有");
                                }
                            });
                        } else {
                            Firevalue.post(new Runnable() {  // 无火
                                @Override
                                public void run() {
                                    Firevalue.setText("无");
                                }
                            });
                        }

                        Tempvalue.post(new Runnable() {  //温度显示
                            @Override
                            public void run() {
                                Tempvalue.setText(mess[2] + "%");
                            }
                        });

                        Humivalue.post(new Runnable() {  //湿度显示
                            @Override
                            public void run() {
                                Humivalue.setText(mess[3] + "℃");
                            }
                        });


                    }

                }
            });
            //连接mqtt服务器
            mqtt_client.connect(options);
            //订阅mqtt服务器
            mqtt_client.subscribe(mqtt_sub_topic,1);
//            mqtt_client.publish(mqtt_sub_topic,new MqttMessage("hello".getBytes()));

            top.setOnTouchListener(new View.OnTouchListener() {    //向上事件监测
                @Override
                public boolean onTouch(View v, MotionEvent event) {
                    switch (event.getAction()) {
                        case MotionEvent.ACTION_DOWN:
                            mqtt_pub(matt_pub_movetop,"top");
                            break;
                        case MotionEvent.ACTION_UP:
                            mqtt_pub(matt_pub_movetop,"stop");
                            break;
                        case MotionEvent.ACTION_MOVE:
                            System.out.println("top移动");
                            break;
                    }
                    return true;
                }
            });

            down.setOnTouchListener(new View.OnTouchListener() {   //向下事件监测
                @Override
                public boolean onTouch(View v, MotionEvent event) {
                    switch (event.getAction()) {
                        case MotionEvent.ACTION_DOWN:
                            mqtt_pub(matt_pub_movetop,"down");
                            break;
                        case MotionEvent.ACTION_UP:
                            mqtt_pub(matt_pub_movetop,"stop");
                            break;
                        case MotionEvent.ACTION_MOVE:
                            System.out.println("down移动");
                            break;
                    }
                    return true;
                }
            });

            left.setOnTouchListener(new View.OnTouchListener() {   //向左事件监测
                @Override
                public boolean onTouch(View v, MotionEvent event) {
                    switch (event.getAction()) {
                        case MotionEvent.ACTION_DOWN:
                            mqtt_pub(matt_pub_movetop,"left");
                            break;
                        case MotionEvent.ACTION_UP:
                            mqtt_pub(matt_pub_movetop,"stop");
                            break;
                        case MotionEvent.ACTION_MOVE:
                            System.out.println("left移动");
                            break;
                    }
                    return true;
                }
            });

            right.setOnTouchListener(new View.OnTouchListener() {   //向右事件监测
                @Override
                public boolean onTouch(View v, MotionEvent event) {
                    switch (event.getAction()) {
                        case MotionEvent.ACTION_DOWN:
                            mqtt_pub(matt_pub_movetop,"right");
                            break;
                        case MotionEvent.ACTION_UP:
                            mqtt_pub(matt_pub_movetop,"stop");
                            break;
                        case MotionEvent.ACTION_MOVE:
                            System.out.println("right移动");
                            break;
                    }
                    return true;
                }
            });

        }catch (Exception e) {
            e.printStackTrace();
            makeToast(e.toString());
            System.out.println("error");

        }
    }

    private void makeToast(String toast_str) {  // Android页面提醒
        Toast.makeText(MainActivity.this, toast_str, Toast.LENGTH_LONG).show();
    }

    public void mqtt_pub(String topic,String order){   // MQTT消息发布
        try {
            mqtt_client.publish(topic,new MqttMessage(order.getBytes()));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void video(){
        webView = (WebView) findViewById(R.id.VideoView);
        //需要加载的网页的url
        webView.loadUrl("http://175.27.245.39:5000/");

        WebSettings settings = webView.getSettings();
        webView.setInitialScale(148);
        // 如果访问的页面中要与Javascript交互，则webview必须设置支持Javascript
        settings.setJavaScriptEnabled(true);
        webView.setWebViewClient(new WebViewClient(){
            public boolean shouldOverrideUrlLoading(WebView view, String url){
                view.loadUrl(url);
                return true;
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
                //等待证书响应
                handler.proceed();
            }
        });
    }

}