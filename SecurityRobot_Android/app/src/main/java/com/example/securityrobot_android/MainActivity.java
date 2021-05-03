package com.example.securityrobot_android;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MainActivity extends AppCompatActivity {

    private String serverUrl = "tcp://175.27.245.39:1883";
    private String userName = "mosquitto";
    private String passWord = "mosquitto";
    private String mqtt_sub_topic = "test";
    private String clientId = "app"+System.currentTimeMillis();
    private MqttClient mqtt_client;                         //创建一个mqtt_client对象
    MqttConnectOptions options;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mqtt_init_Connect();
        makeToast("MQTT连接成功");
    }

    public void mqtt_init_Connect()
    {
        try {
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
                    makeToast("connectionLost");

                }
                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {
                    //publish后会执行到这里
                    System.out.println("发送成功");
                }
                @Override
                public void messageArrived(String topicName, MqttMessage message) throws Exception {
                    //subscribe后得到的消息会执行到这里面
                    System.out.println("接收消息主题 : " + topicName);
                    System.out.println("接收消息Qos : " + message.getQos());
                    System.out.println("接收消息内容 : " + new String(message.getPayload()));
                }
            });
            //连接mqtt服务器
            mqtt_client.connect(options);
            //订阅mqtt服务器
            mqtt_client.subscribe(mqtt_sub_topic,1);
//            mqtt_client.publish(mqtt_sub_topic,new MqttMessage("hello".getBytes()));

        }catch (Exception e) {
            e.printStackTrace();
            makeToast(e.toString());
        }
    }

    private void makeToast(String toast_str) {  //页面提醒
        Toast.makeText(MainActivity.this, toast_str, Toast.LENGTH_LONG).show();
    }


}