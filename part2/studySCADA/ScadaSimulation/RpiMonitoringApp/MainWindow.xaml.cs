using MahApps.Metro.Controls;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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
using System.Diagnostics;
using SmartHomeMonitoringApp.Views;
using MahApps.Metro.Controls.Dialogs;
using SmartHomeMonitoringApp.Logics;
using System.ComponentModel;
using ControlzEx.Theming;

namespace SmartHomeMonitoringApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        string DefaultTheme { get; set; } = "Light";    
        string DefaultAccent { get; set; } = ":Cobalt";
        public MainWindow()
        {
            InitializeComponent();

            ThemeManager.Current.ThemeSyncMode = ThemeSyncMode.SyncWithAppMode;
            ThemeManager.Current.SyncTheme();
        }

        private void MetroWindow_Loaded(object sender, RoutedEventArgs e)
        {
            //<Frame> ==> Page.xaml
            //<ContentContro> ==> UserControl.xaml
            //ActiveItem.Content = new Views.DataBaseControl();
        }


        private void MnuExitProgram_Click(object sender, RoutedEventArgs e)
        {
           Environment.Exit(0); // 둘중하나만 쓰면 됨
           System.Diagnostics.Process.GetCurrentProcess().Kill();  // 작업관리자에서 프로세스 종료!
        }

        // MQTT 시작 메뉴 클릭 이벤트 핸들러
        private void MnuStartSubscribe_Click(object sender, RoutedEventArgs e)
        {
            var mqttPopWin = new MqttPopupWindow();
            mqttPopWin.Owner = this;
            mqttPopWin.WindowStartupLocation = WindowStartupLocation.CenterOwner;
            var result = mqttPopWin.ShowDialog();

            if (result == true)
            {
                var userControl = new Views.DataBaseControl();
                ActiveItem.Content = userControl;
                StsSelScreen.Content = "DataBase Monitoring"; //typeof(Views.DataBaseControl);
            }
        }

        private async void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            // e.Cancel을 true 하고 시작
            e.Cancel = true;

            var mySettings = new MetroDialogSettings
            { AffirmativeButtonText = "끝내기", NegativeButtonText = "취소", AnimateShow = true, AnimateHide = true };

             var result = await this.ShowMessageAsync("프로그램 끝내기","프로그램을 끝내시겠습니까?", 
                                                    MessageDialogStyle.AffirmativeAndNegative, mySettings);
             if(result == MessageDialogResult.Negative)
            {e.Cancel = true;}
            else
            {
                if(Commons.MQTT_CLIENT !=null && Commons.MQTT_CLIENT.IsConnected)
                {
                    Commons.MQTT_CLIENT.Disconnect(); 
                }Process.GetCurrentProcess().Kill();
            } //가장 확실


        }

        private void BtnExitProgram_Click(object sender, RoutedEventArgs e)
        {
            // 확인 메시지 윈도우 클로징 이벤트 헨들러 호출
            this.MetroWindow_Closing(sender, new CancelEventArgs());
        }

        private void MnuDataBaseMon_Click(object sender, RoutedEventArgs e)
        {
            var userControl = new Views.DataBaseControl();
            ActiveItem.Content = userControl;
            StsSelScreen.Content = "DataBase Monitoring"; //typeof(Views.DataBaseControl);
        }

        private void MnuRealTimeMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.RealTimeControl();
            StsSelScreen.Content = "RealTime Monitoring";
        }

        private void MnuvisualizationMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.VisualizationControl();
            StsSelScreen.Content = "Visualization View";
        }

        private void MnuAbout_Click(object sender, RoutedEventArgs e)
        {
            var about = new About();
            about.Owner = this;
            about.ShowDialog();
        }

        // 모든 테마와 액센트를 전부처리할 체크이벤트 핸들러
        private void MnuThemeAceent_Checked(object sender, RoutedEventArgs e)
        {         
            // 클릭되는 테마가 라이트인지 다크인지 판단/라이트를 클릭하면 다크는 체크해제, 다크를 클릭하면 라이트를 체크해제
            Debug.WriteLine((sender as MenuItem).Header);
            // 액센트도 체크를 하는값을 나머지 액센트 체크해제
            switch ((sender as MenuItem).Header)
            {
                case "Light":
                    MnuLightTheme.IsChecked = true;
                    MnuDarkThmem.IsChecked = false;
                    DefaultTheme = "Light";
                    break;
                case "Dark":
                    MnuLightTheme.IsChecked = false;
                    MnuDarkThmem.IsChecked= true;
                    DefaultTheme = "Dark";
                    break;
                case "Amber":
                    MnuAccentAmber.IsChecked = true;
                    MnuAccentBlue.IsChecked = false;
                    MnuAccentBrown.IsChecked = false;
                    MnuAccentCobalt.IsChecked = false;
                    DefaultTheme = "Amber";

                    break;
                case "Blue":
                    MnuAccentAmber.IsChecked = false;
                    MnuAccentBlue.IsChecked = true;
                    MnuAccentBrown.IsChecked = false;
                    MnuAccentCobalt.IsChecked = false;
                    DefaultTheme = "Blue";

                    break;
                case "Brown":
                    MnuAccentAmber.IsChecked = false;
                    MnuAccentBlue.IsChecked = false;
                    MnuAccentBrown.IsChecked = true;
                    MnuAccentCobalt.IsChecked = false;
                    DefaultTheme = "Brown";

                    break;
                case "Cobalt":
                    MnuAccentAmber.IsChecked = false;
                    MnuAccentBlue.IsChecked = false;
                    MnuAccentBrown.IsChecked = false;
                    MnuAccentCobalt.IsChecked = true;
                    DefaultTheme = "Cobalt";

                    break; 
            }
                ThemeManager.Current.ChangeTheme(this, "Dark.Amber");
        }
    }
}
