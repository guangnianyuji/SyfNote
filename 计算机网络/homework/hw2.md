##### **1. ARQ (20 points)**

**Consider the data transmission from sender A to receiver B via the Go-Back-N (with NAK) protocol with a large window size N (so that packet transmissions will not be limited by the window size).**

**a) Fill in the boxes of the figure below. Write the packet number in the form of Px, and the response in the form of ACKx or NAKx. (14 points)**

- Lost frame: may cause timeout or NAK, maybe not;
- Lost ACK: It is okay if later ACK is received, otherwise cause timeout;
- Timeout: If timer counts down to zero without receiving the right frame, the sender should repeating sending.

**b) Write the corresponding actions (A for Accept, DD for discard as duplicates, DE for discard as error) for each packet at the receiver end. (6 points)**

The receive window has size of 1, and only receiving the right frame it waits  makes the situation **Accept**;Receiving the frame it has received is the situation **Discard as Duplicates**; Others are treated as **Discard as Errors**;

![image-20231128192632009](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231128192632009.png)

**2. Medium Access Control (25 points, 5 points each)**

**Briefly answer the following questions in your own words.**

**a) Describe the CSMA/CA mechanism used in IEEE 802.11 (WiFi). You may draw a diagram, describe in words, or write pseudo code for this.**



**Sender:**

1. If sender senses the channel idle for DIFS, then transmit the entire frame.

   Otherwise,sender starts random backoff interval,by a timer.

2. Timer counts down when channel is idle,and freezes when channel is busy.

3. When Timer counts to zero,transmit the entire frame.

4. If an ACK is received by sender,go to step 1 to transmit the next frame;

   If an ACK is not received by sender,increase backoff interval , go to step 2 , to transmit the same frame again.

**Receiver:**

​	If the frame is successfully received, replies an ACK after SIFS.



**b) Why can’t we use CSMA/CD in wireless LAN?**

1. The received signal strength is often much weaker than the transmitted signal strength, and the signal strength can vary significantly in wireless media. Therefore, implementing **collision detection in hardware would require significant cost**.

2. In wireless communication, not all stations can hear each other, resulting in the **"hidden terminal" problem**.

   

**c) Why do we need the RTS-CTS mechanism?**

For example,station A and B are both within the range of radio of AP(Access Point), but they can not hear each other. They both see that channel is idle and begin transmitting something to AP at the same time,so that collision occurs.

When use the RTS-CTS mechanism,the protocol starts when station A wants to send data to AP. Firstly, A **send** a  RTS(Request to Send) frame to AP to request permission to send it a frame. If AP receive the request,will **send** a  CTS(Clear to Send)  frame back. And all the stations including A within range of the radio of  AP  can **hear** it. So other stations will  estimate how long this turn of data exchange will take according to the information in the CTS. During this period, other stations **will not transmit** anything until the exchange is completed.

**d) How does a bridge learn the hosts in a LAN? (Hint: Read Chapter 4.8.2 and 4.8.3 in the**

**textbook)**

1. **Initial State**: When a bridge is first powered on, its forwarding table is empty.
2. **Bridge uses the backward learning algorithm**: By learning every frame sent on its ports,bridge can tell the source address of the frame can be accessible on the port the frame comes. And  bridge will add an entry to the forwarding table.
3. **Routing procedure**: 

   1. If the destination port is known( in the forwarding table), and the port for the destination address is the same as the **source** port,**discard** the frame.

   2. If the destination port is known( in the forwarding table), and the destination address and the source port are **different**, forward the frame on to the destination port.

   3. If the destination port is **unknown**, use **flooding** and send the frame on all ports except the source port. 
4. **Aging out old entries**: The forwarding table entries have a certain aging time. If an entry is not refreshed (by frames from the same source MAC address being seen again) within a certain time, the entry is removed from the table. This ensures that the table is kept up-to-date with only active hosts.
4. **Spanning Trees**: To avoid loops, bridges run the spanning tree algorithm to build a spanning tree topology structure, ensuring only one way between every pair of hosts.

**e) What are the differences between a bridge/switch and a hub? (Hint: Read Chapter 4.8.4**

**in the textbook)**

1. **Hub**:
   - **Layer**: Operates at the physical layer (Layer 1) of the OSI model.
   - **Functionality**: A hub broadcasts incoming data packets to **all other ports** regardless of the destination address, which can lead to a lot of unnecessary traffic on the network.
   - **Collision Domain**: All ports on a hub belong to the same collision domain, meaning that if two devices transmit at the same time, a collision will occur.
   - **Buffering**: None.
   - **Connectivity**: Only the same type of networks.
2. **Bridge**:
   - **Layer**: Operates at the data link layer (Layer 2) of the OSI model.
   - **Functionality**: A bridge divides a network into segments and determines the flow of traffic based on MAC addresses. It can reduce the amount of traffic on a network by deciding whether or not to forward traffic based on the destination address of each data frame. And a bridge **can decide** which port transmits the frame to according to its forwarding table.  
   - **Collision Domain**: Bridges create separate collision domains for each port, which reduces the chances of collisions.
   - **Buffering**: Queue frames between different speed ports.
   - **Connectivity**: It can connect different types of networks. 

**3. IP Addressing (10 points)**

Briefly answer the following questions.

**a) For a network with IP address 192.168.8.0/26, how many host IP addresses can be assigned** **in this network? (3 points)**

​	In an IPv4 address, there are a total of 32 bits. If 26 bits are used for the network address, then 32 - 26 = 6 bits are left for host addresses.

​	And Subtract the network address of all 1s address, the broadcasting address of all 0s address.

​	So the answer is $2^6-2=62$.

**b) With respect to the number of destinations, IP addresses can be categorized into three** **types. What are they? Give an example for each type of addresses. (4 points)**

1. **Unicast Addresses**:
   - **Description**: A unicast address identifies a single unique node on a network. It is used for one-to-one communication, where a packet is sent from one single host to another single host.
   - **Example**: `192.168.1.10` - This address would refer to a single device on a local network.
2. **Broadcast Addresses**:
   - **Description**: A broadcast address allows transmission of a packet to all nodes on a network. In IPv4, it is the last address in a network range that is used to address all hosts in that network simultaneously.
   - **Example**: `192.168.1.255` (assuming the subnet mask is `255.255.255.0`) - This address is used to send data to all hosts on the `192.168.1.0` network.
3. **Multicast Addresses**:
   - **Description**: A multicast address is used to deliver a packet to a group of destinations that are part of a multicast group. It can be used for one-to-many communication, where a packet is delivered to multiple hosts who are **listening to** the multicast address.
   - **Example**: `224.0.0.1` - This address is a reserved multicast group address to which all IPv4-enabled devices belong.

**c) ARP is an aiding protocol for IP. Describe in your own words how ARP request and ARP reply works. (3 points)**

Host A wants to send a packet to Host B which is in the same LAN with A(in the network layer).

1. Host A checks if the IP address in its ARP cache.

2. 1 If there is the IP address in its ARP cache,find out the corresponding MAC address,and  write  to the MAC frame, and then send the MAC frame to destination MAC address through the LAN.

3. 2  If not,use destination MAC address FFFF-FF-FF-FF-FF to broadcast the APR request and all the hosts on LAN receive the request.

   Then After receiving the ARP request, host B sends the ARP response packet (unicast delivery) to host A, which contains the mapping relationship between the IP of host B and the MAC address. 

   After host A receives the ARP response packet, host A will write the mapping to the ARP cache,and do the Step 2.

**4. Routing: Dijkstra (20 points)**

Consider the network topology as follow.

![image-20231123221614817](C:/Users/sunyifei/AppData/Roaming/Typora/typora-user-images/image-20231123221614817.png)

**a) Describe the Dijkstra algorithm with pseudo code. (5 points)**

```
#initialization
N<-{s}
for v not in N do:
	D(v)<-l(s,v)
#compute
while there is remaining nodes that are not in N do:
	w<-argmin {D(v)| v is not in N}
	N<-N U {w}
    for v not in N do:
		D(v)<-min{D(w)+l(w,v),D(v)}	
```

**b) Find the shortest path from node A to all the other nodes in the network with the Dijkstra** **algorithm. Make sure you show all your steps (with the table!). (10 points)**

| Step | Set N       | D(B),p(B) | D(C),p(c) | D(D),p(D) | **D(E), p(E)** | **D(F), p(F)** |
| ---- | ----------- | --------- | --------- | --------- | -------------- | -------------- |
| 0    | A           | 4,A       | 1,A       | ∞         | ∞              | ∞              |
| 1    | A,C         | 3,C       | 1,A       | ∞         | 4,C            | ∞              |
| 2    | A,C,B       | 3,C       | 1,A       | 8,B       | 4,C            | 12,B           |
| 3    | A,C,B,E     | 3,C       | 1,A       | 5,E       | 4,C            | 7,E            |
| 4    | A,C,B,E,D   | 3,C       | 1,A       | 5,E       | 4,C            | 6,D            |
| 5    | A,C,B,E,D,F | 3,C       | 1,A       | 5,E       | 4,C            | 6,D            |

The shortest path from node A to all the other nodes are as follows:

B: A->C->B   3

C: A->C 1

D: A->C->E->D 5

E: A->C->E 4

F: A->C->E->D->F  6

**c) Consider a networking condition in which you are asked to write an algorithm to find the most reliable path, i.e., the path with the least Bit Error Rate (BER). Assume each link in the network has a BER (in the range of 0 and 1) that is independent of other links.**

**Can we directly use Dijkstra algorithm? If not, how to change it to solve this problem? (5 points)**

Exactly, $BER\_path=1-\prod(1-BER_i)$.Minimize $BER\_path$=>Minimize $-\prod(1-BER_i)$=>Minimize $\sum-\log{(1-BER_i)}$.

If **a BER of 1 occurs**, it indicates a totally broken link. The negative logarithm of 0 is undefined, so we can either set it to a very small negative value or handle it as a special case to indicate a totally broken link.

The Dijkstra algorithm is designed to find the shortest path between nodes in a graph, which can be used when the path cost is additive.

Then we can use Dijkstra algorithm,to find the min $\sum -\log{(1-BER_i)}$ path.

##### **5. Routing: Bellman-Ford (10 points)**

**Consider the same network topology as in Question 4, and find the shortest path to node A with the Bellman-Ford algorithm. Update Order B *→* C *→* D *→* E *→* F. Make sure you show all your steps (with the table!).**

| Cycle | n(B),D(B) | n(C),D(C) | n(D),D(D) | n(E),D(E) | n(F),D(F) |
| ----- | --------- | --------- | --------- | --------- | --------- |
| 0     | (∙ , ∞)   | (∙ , ∞)   | (∙ , ∞)   | (∙ , ∞)   | (∙ , ∞)   |
| 1     | (A,4)     | (A,1)     | (B,9)     | (C,4)     | (E,7)     |
| 2     | (C,3)     | (A,1)     | (D,5)     | (C,4)     | (D,6)     |
| 3     | (C,3)     | (A,1)     | (D,5)     | (C,4)     | (D,6)     |

The shortest path from node A to all the other nodes are as follows:

B: A->C->B   3

C: A->C 1

D: A->C->E->D 5

E: A->C->E 4

F: A->C->E->D->F  6

**6. QoS (15 points)**

Give real-world examples for the following scheduling schemes.

**a) FIFO Queue (4 points)**

**Ticket Counters:** At ticket counters, people line up to purchase tickets. The first person in line is the first to receive a ticket.

**b) Priority Queue (4 points)**

**Task Scheduling In Operating Systems:** In operating systems and job schedulers, tasks with higher priority are executed before those with lower priority.

**c) Round Robin (4 points)**

**Process Scheduling In Operating Systems:** Round-robin scheduling is to limit the execution time of each process to a short period of time, at which point the process hangs and another process takes its turn.

**d) Weighted Fair Queue (WFQ) (3 points)**

**Weighted Fair Queue in packet scheduling:** It  serves in a circular manner, giving the high-priority queue a large weight which represents more bytes per round. It can guarantee bandwidth for each flow.