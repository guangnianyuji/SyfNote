#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include <fstream>
#include "ns3/ipv6-static-routing-helper.h"
#include "ns3/ipv6-routing-table-entry.h"
#include "ns3/internet-module.h"
#include "ns3/tcp-header.h"
#include "ns3/traffic-control-module.h"
#include  <string>
#include "ns3/netanim-module.h"
#include "ns3/flow-monitor-module.h"

// Dumbbell topology with 7 senders and 1 receiver
// is used for this example. On successful completion,
// the Congestion window and Queue size traces get stored
// in MixTraffic/ directory, inside cwndTraces and
// queueTraces sub-directories, respectively.

using namespace ns3;

std::string dir = "MixTraffic/";

void
CheckQueueSize (Ptr<QueueDisc> queue,std::string queue_disc_type)
{
  double qSize = queue->GetCurrentSize ().GetValue ();
  // check queue size every 1/10 of a second
  Simulator::Schedule (Seconds (0.1), &CheckQueueSize, queue, queue_disc_type);

  std::ofstream fPlotQueue (dir + queue_disc_type + "/queueTraces/queue.plotme", std::ios::out | std::ios::app);
  fPlotQueue << Simulator::Now ().GetSeconds () << " " << qSize << std::endl;
  fPlotQueue.close ();
}

static void
CwndTrace (Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
  *stream->GetStream () << Simulator::Now ().GetSeconds () << " " << newCwnd / 1446.0 << std::endl;
}

static void
TraceCwnd (std::string queue_disc_type)
{
  for (uint8_t i = 0; i < 5; i++)
    {
      AsciiTraceHelper asciiTraceHelper;
      Ptr<OutputStreamWrapper> stream = asciiTraceHelper.CreateFileStream (dir + queue_disc_type + "/cwndTraces/S1-" + std::to_string (i + 1) + ".plotme");
      Config::ConnectWithoutContext ("/NodeList/" + std::to_string (i) + "/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow", MakeBoundCallback (&CwndTrace,stream));
    }
}

#define TCPNUM 6
#define UDPNUM 2
#define GROUPNUM 2
#define SINKNUM 4
void experiment (std::string queue_disc_type)
{
  // Set the simulation stop time in seconds
  double stopTime = 101;
  std::string queue_disc = std::string ("ns3::") + queue_disc_type;

  std::string bottleneckBandwidth = "10Mbps";
  std::string bottleneckDelay = "50ms";

  std::string accessBandwidth = "10Mbps";
  std::string accessDelay = "5ms";

  // Create sender
  NodeContainer tcpSender[GROUPNUM];
  for(int i=0;i<GROUPNUM;i++)
  {
      tcpSender[i].Create (TCPNUM);
  }


  NodeContainer udpSender[2];
  for(int i=0;i<GROUPNUM;i++)
  {
      udpSender[i].Create (UDPNUM);
  }

  // Create gateway
  NodeContainer gateway;
  gateway.Create (3);

  // Create sink
  NodeContainer sink;
  sink.Create (SINKNUM);

  Config::SetDefault ("ns3::TcpSocket::SndBufSize", UintegerValue (1 << 20));
  Config::SetDefault ("ns3::TcpSocket::RcvBufSize", UintegerValue (1 << 20));
  Config::SetDefault ("ns3::TcpSocket::DelAckTimeout", TimeValue (Seconds (0)));
  Config::SetDefault ("ns3::TcpSocket::InitialCwnd", UintegerValue (1));
  Config::SetDefault ("ns3::TcpSocketBase::LimitedTransmit", BooleanValue (false));
  Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (1446));
  Config::SetDefault ("ns3::TcpSocketBase::WindowScaling", BooleanValue (true));
  Config::SetDefault (queue_disc + "::MaxSize", QueueSizeValue (QueueSize ("200p")));

  InternetStackHelper internet;
  internet.InstallAll ();

  TrafficControlHelper tchPfifo;
  uint16_t handle = tchPfifo.SetRootQueueDisc ("ns3::PfifoFastQueueDisc");
  tchPfifo.AddInternalQueues (handle, 3, "ns3::DropTailQueue", "MaxSize", StringValue ("1000p"));

  TrafficControlHelper tch;
  tch.SetRootQueueDisc (queue_disc);

  PointToPointHelper accessLink;
  accessLink.SetDeviceAttribute ("DataRate", StringValue (accessBandwidth));
  accessLink.SetChannelAttribute ("Delay", StringValue (accessDelay));

  // Configure the senders and sinks net devices
  // and the channels between the senders/sinks and the gateways
  NetDeviceContainer devices [GROUPNUM][TCPNUM];
  for (int j=0;j<GROUPNUM;j++)
  {
  for (uint8_t i = 0; i < TCPNUM; i++)
    {
      devices [j][i] = accessLink.Install (tcpSender[j].Get (i), gateway.Get (j));
      tchPfifo.Install (devices[j] [i]);
    }
  }

  NetDeviceContainer devices_sink[SINKNUM];
  for(int i=0;i<SINKNUM;i++)
  {
  devices_sink[i] = accessLink.Install (gateway.Get (2), sink.Get (i));
  tchPfifo.Install (devices_sink[i]);
  }
 

  PointToPointHelper bottleneckLink;
  bottleneckLink.SetDeviceAttribute ("DataRate", StringValue (bottleneckBandwidth));
  bottleneckLink.SetChannelAttribute ("Delay", StringValue (bottleneckDelay));

  NetDeviceContainer devices_gateway[GROUPNUM];
  devices_gateway[0] = bottleneckLink.Install (gateway.Get (0), gateway.Get (2));
  devices_gateway[1] = bottleneckLink.Install (gateway.Get (1), gateway.Get (2));
  // Install QueueDisc at gateway
  QueueDiscContainer queueDiscs = tch.Install (devices_gateway[0]);
  tch.Install( devices_gateway[1].Get(0));

  Ipv4AddressHelper address;
  address.SetBase ("10.0.0.0", "255.255.255.0");

  Ipv4InterfaceContainer interfaces [GROUPNUM][TCPNUM];
  Ipv4InterfaceContainer interfaces_sink[SINKNUM];
  Ipv4InterfaceContainer interfaces_gateway;
  Ipv4InterfaceContainer udpinterfaces [GROUPNUM][UDPNUM];

  NetDeviceContainer udpdevices [GROUPNUM][UDPNUM];

  for (int j=0;j<GROUPNUM;j++)
  {
  for (uint8_t i = 0; i < TCPNUM; i++)
    {
      address.NewNetwork ();
      interfaces[j][i] = address.Assign (devices[j][i]);
    }
  }

  for(int j=0;j<GROUPNUM;j++)
  {
  for (uint8_t i = 0; i < UDPNUM; i++)
    {
      udpdevices[j][i] = accessLink.Install (udpSender[j].Get (i), gateway.Get (j));
      address.NewNetwork ();
      udpinterfaces[j][i] = address.Assign (udpdevices[j][i]);
    }
  }
    for(int j=0;j<GROUPNUM;j++)
  {
  address.NewNetwork ();
  interfaces_gateway = address.Assign (devices_gateway[j]);
  }

  address.NewNetwork ();
  for (int i=0;i<SINKNUM;i++)
  {
     address.NewNetwork ();
    interfaces_sink[i] = address.Assign (devices_sink[i]);
  }
 
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  uint16_t port = 50000;
  uint16_t port1 = 50001;
  Address sinkLocalAddress (InetSocketAddress (Ipv4Address::GetAny (), port));
  Address sinkLocalAddress1 (InetSocketAddress (Ipv4Address::GetAny (), port1));
  PacketSinkHelper sinkHelper ("ns3::TcpSocketFactory", sinkLocalAddress);
  PacketSinkHelper sinkHelper1 ("ns3::UdpSocketFactory", sinkLocalAddress1);

  for(int i=0;i<SINKNUM;i++)
  {
      AddressValue remoteAddress (InetSocketAddress (interfaces_sink[i].GetAddress (1), port));

      BulkSendHelper ftp ("ns3::TcpSocketFactory", Address ());
      ftp.SetAttribute ("Remote", remoteAddress);
      ftp.SetAttribute ("SendSize", UintegerValue (1000));
      
      ApplicationContainer sourceApp;
      int offset=0;
      if(i%2)
      {
        offset=3;
      }
      for(int j=0;j<3;j++)
      {
        sourceApp.Add(ftp.Install(tcpSender[i/2].Get(j+offset)));
      }
      sourceApp.Start (Seconds (0));
      sourceApp.Stop (Seconds (stopTime - 1));

      sinkHelper.SetAttribute ("Protocol", TypeIdValue (TcpSocketFactory::GetTypeId ()));
      ApplicationContainer sinkApp = sinkHelper.Install (sink.Get(i));
      sinkApp.Start (Seconds (0));
      sinkApp.Stop (Seconds (stopTime));

  }
  
  for(int i=0;i<SINKNUM;i++)
  {
  OnOffHelper clientHelper6 ("ns3::UdpSocketFactory", Address ());
  clientHelper6.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
  clientHelper6.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
  clientHelper6.SetAttribute ("DataRate", DataRateValue (DataRate ("10Mb/s")));
  clientHelper6.SetAttribute ("PacketSize", UintegerValue (1000));

  AddressValue remoteAddress1 (InetSocketAddress (interfaces_sink[i].GetAddress (1), port1));

  ApplicationContainer clientApps6;
  clientHelper6.SetAttribute ("Remote", remoteAddress1);
  clientApps6.Add (clientHelper6.Install (udpSender[i/2].Get (i%2)));
  clientApps6.Start (Seconds (0));
  clientApps6.Stop (Seconds (stopTime - 1));

  sinkHelper1.SetAttribute ("Protocol", TypeIdValue (UdpSocketFactory::GetTypeId ()));
  ApplicationContainer sinkApp1 = sinkHelper1.Install (sink.Get(i));
  sinkApp1.Start (Seconds (0));
  sinkApp1.Stop (Seconds (stopTime));
  }

  Ptr<QueueDisc> queue = queueDiscs.Get (0);//只看一个链路的情况
  Simulator::ScheduleNow (&CheckQueueSize, queue,queue_disc_type);

  std::string dirToSave = "mkdir -p " + dir + queue_disc_type;
  if (system ((dirToSave + "/cwndTraces/").c_str ()) == -1
      || system ((dirToSave + "/queueTraces/").c_str ()) == -1)
    {
      exit (1);
    }

    
      for (int i = 0; i < TCPNUM; ++i){
      AnimationInterface::SetConstantPosition(tcpSender[0].Get(i), 20, 20 + i * 10);
      AnimationInterface::SetConstantPosition(tcpSender[1].Get(i), 80, 20 + i * 10);
       
    }

      for (int i = 0; i < UDPNUM; ++i){
      AnimationInterface::SetConstantPosition(udpSender[0].Get(i), 20, 20 + (i+6) * 10);
      AnimationInterface::SetConstantPosition(udpSender[1].Get(i), 80, 20 + (i+6) * 10);   
    }

          for (int i = 0; i < SINKNUM; ++i){
      AnimationInterface::SetConstantPosition(sink.Get(i), 20, 20 + (i+6) * 10);
       AnimationInterface::SetConstantPosition(sink.Get(i),50 + (i - (SINKNUM+1) / 2) * 10, 80);
    }

    AnimationInterface::SetConstantPosition(gateway.Get(0), 40, 15 + 5 * 4);
    AnimationInterface::SetConstantPosition(gateway.Get(1), 60, 15 + 5 * 4);
    AnimationInterface::SetConstantPosition(gateway.Get(2), 50, 60);
 
 AnimationInterface anim ("lab2.xml");
    uint32_t hostLogo= anim.AddResource("../ns-3.35/scratch/host.png");
    uint32_t switchLogo = anim.AddResource("../ns-3.35/scratch/switch.png");
    uint32_t routerLogo = anim.AddResource("../ns-3.35/scratch/router.png");

          for (int i = 0; i < TCPNUM; ++i){
           anim.UpdateNodeSize(tcpSender[0].Get(i)->GetId(),6,6);
            anim.UpdateNodeImage(tcpSender[0].Get(i)->GetId(), hostLogo);
            anim.UpdateNodeSize(tcpSender[1].Get(i)->GetId(),6,6);
           anim.UpdateNodeImage(tcpSender[1].Get(i)->GetId(), hostLogo);
    }

              for (int i = 0; i < UDPNUM; ++i){
           anim.UpdateNodeSize(udpSender[0].Get(i)->GetId(),6,6);
          anim.UpdateNodeImage(udpSender[0].Get(i)->GetId(), hostLogo);
           anim.UpdateNodeSize(udpSender[1].Get(i)->GetId(),6,6);
           anim.UpdateNodeImage(udpSender[1].Get(i)->GetId(), hostLogo);
    }


          for (int i = 0; i < SINKNUM; ++i){
           anim.UpdateNodeSize(sink.Get(i)->GetId(),6,6);
           anim.UpdateNodeImage(sink.Get(i)->GetId(), hostLogo);
    }
     for (int i = 0; i <3; ++i)
     {
           anim.UpdateNodeSize(gateway.Get(i)->GetId(),6,6);
           anim.UpdateNodeImage(gateway.Get(i)->GetId(), routerLogo);
     }

  Simulator::Schedule (Seconds (0.1), &TraceCwnd,queue_disc_type);

  Simulator::Stop (Seconds (stopTime));
  // 创建FlowMonitorHelper对象
FlowMonitorHelper flowHelper;
// 安装一个FlowMonitor实例到所有节点
Ptr<FlowMonitor> monitor = flowHelper.InstallAll();
 
  Simulator::Run ();
//暂时未成功
// // 创建FlowMonitorHelper对象
// FlowMonitorHelper flowHelper;
// // 安装一个FlowMonitor实例到所有节点
// Ptr<FlowMonitor> monitor = flowHelper.InstallAll();

  // 收集并报告流量统计信息
monitor->CheckForLostPackets(); // 检查丢失的数据包

Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowHelper.GetClassifier());
std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();

// 初始化变量以存储总的发送和接收的字节及丢失的数据包数量
uint64_t totalTxBytes = 0;
uint64_t totalRxBytes = 0;
uint64_t totalLostPackets = 0;
double totalDelaySum = 0;
uint64_t totalRxPackets = 0;

for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i)
{
    // 累加每个流的发送和接收的字节及丢失的数据包数量
    totalTxBytes += i->second.txBytes;
    totalRxBytes += i->second.rxBytes;
    totalLostPackets += i->second.lostPackets;
    totalDelaySum += i->second.delaySum.GetSeconds();
    totalRxPackets += i->second.rxPackets;
}

// 计算总吞吐量、平均延迟和总丢包率
double totalTime = stopTime;
double totalThroughput = totalRxBytes * 8.0 / totalTime / 1024 / 1024; // Mbps
double averageDelay = totalRxPackets > 0 ? totalDelaySum / totalRxPackets : 0; // seconds
double totalLossRate = totalTxBytes > 0 ? (static_cast<double>(totalLostPackets) / totalTxBytes * 8) * 100 : 0; // %

// 打印总体性能指标
std::cout << "总发送字节: " << totalTxBytes << "\n";
std::cout << "总接收字节: " << totalRxBytes << "\n";
std::cout << "总吞吐量: " << totalThroughput << " Mbps\n";
std::cout << "平均延迟: " << averageDelay << " s\n";
std::cout << "总丢包率: " << totalLossRate << "%\n";
  Simulator::Destroy ();
}

int main (int argc, char **argv)
{
  //experiment ("RedQueueDisc");
  experiment ("PieQueueDisc");
  return 0;
}
