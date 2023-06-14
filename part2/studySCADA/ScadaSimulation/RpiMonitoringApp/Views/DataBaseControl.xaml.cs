using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        public bool IsConnected { get; set; }   // 없으면 UI컨트롤이 어려워짐
        // MQTT Subscribition text 과도문제 속도저하를 잡기위해 변수
        // 23.05.11 09:29
        int MaxCount { get; set; } = 10;

        Thread MqttThread { get; set; }
        public DataBaseControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false;    //아직 접속안되어있음.
            BtnConnDb.IsChecked = false;

            //실시간 모니터링에서 넘어왔을 때
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {
                IsConnected = true;
                BtnConnDb.Content = "MQTT 연결중";
                BtnConnDb.IsChecked = true;
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
        }




        // 토글 버튼 클릭이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            ConnectDB();
            
        }
        private void ConnectDB()
        {
            if (IsConnected == false)
            {
                BtnConnDb.IsChecked = true;
                IsConnected = true;

                // Mqtt 브로커생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    //MqTT subscribe(구독할) 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        // Mqtt 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR");     // clientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                            new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE }); // QO는 네트워크 통신에 옵션
                        UpdateLog(">>> MQTT Broker Connected");

                        BtnConnDb.IsChecked = true;
                        BtnConnDb.Content = "MQTT 연결중";
                        IsConnected = true; //예외발생하면 true로 변경할 필요 없음
                    }

                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT Error 발생 : {ex.Message}");
                    //Pass;
                }
            }
            else
            {
                try
                {
                    if (Commons.MQTT_CLIENT.IsConnected)
                    {
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Disconnect();
                        UpdateLog(">>> MQTT Broker Disconnected...");

                        BtnConnDb.IsChecked = false;
                        BtnConnDb.Content = "MQTT 연결종료";
                        IsConnected = false;
                    }

                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT Error 발생 :{ex.Message}");
                }

            }
        }

        private void UpdateLog(string msg)
        {
            this.Invoke(() =>
            {
                if (MaxCount <= 0)
                {
                    TxtLog.Text = string.Empty;
                    TxtLog.Text += ">>> 문서 건수가 많아져서 초기화\n";
                    TxtLog.ScrollToEnd();
                    MaxCount = 10; //테스트할땐 10, 운영시는 50
                }
                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
                MaxCount--;
            });
        }


        // Subscribe가 발생했을 때 이벤트 핸들러
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDateBase(msg, e.Topic);    // 실제 DB에 저장처리
        }

        // DB 저장처리 메서드
        private void SetToDateBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null )
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);

                // Living
                var tmp = currValue["STAT"].Split('|'); // 29.0|45.0 잘라준다음
                var temp = tmp[0].Trim();   // 29.0 trim() 공백제거
                var humid = tmp[1].Trim(); // 45.0 trim() 공백제거
                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING)) 
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = @"INSERT INTO smarthomesensor 
                                            (Home_Id,
                                            Room_Name,
                                            Sensing_DateTime,
                                            Temp,
                                            Humid)
                                            VALUES
                                            (@Home_Id,
                                             @Room_Name,
                                             @Sensing_DateTime,
                                             @Temp,
                                             @Humid)";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["DEV_ID"]);
                        cmd.Parameters.AddWithValue("@Room_Name", "Living");
                        cmd.Parameters.AddWithValue("@Sensing_DateTime", currValue["CURR_DT"]);
                        cmd.Parameters.AddWithValue("@Temp", temp);
                        cmd.Parameters.AddWithValue("@Humid", humid);
                        
                        // ... 파라미터 다섯개
                        if (cmd.ExecuteNonQuery() ==1)
                        {
                            UpdateLog(">>> DB Insert succeed.");
                        }
                        else
                        {
                            UpdateLog(">>> DB Insert failed."); // 일어날일이 거의없음
                        }
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! DB Error 발생 : {ex.Message}");
                }
                
            }
        }
    }
}
