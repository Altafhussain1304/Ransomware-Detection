import 'package:flutter/material.dart';
import 'package:ransom_saver/services/api_service.dart';
import 'package:ransom_saver/widgets/threat_meter.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int index = 0;
  bool drawerOpen = false;
  bool isMonitoring = false;
  late Future<Map<String, dynamic>> summary;

  @override
  void initState() {
    super.initState();
    summary = ApiService().getSummary();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: Center(
          child: DrawerButton(
            style: IconButton.styleFrom(
                iconSize: 25, overlayColor: Colors.transparent),
            onPressed: () {
              setState(() {
                drawerOpen = !drawerOpen;
              });
            },
          ),
        ),
        toolbarHeight: 35,
        leadingWidth: 60,
      ),
      body: Row(
        children: [
          AnimatedContainer(
            duration: Durations.medium4,
            width: drawerOpen ? 250 : 60,
            child: NavigationRail(
              groupAlignment: -1,
              extended: drawerOpen,
              destinations: const [
                NavigationRailDestination(
                  padding: EdgeInsets.symmetric(horizontal: 10),
                  icon: Icon(Icons.home),
                  label: Text('Home'),
                ),
                NavigationRailDestination(
                    padding: EdgeInsets.symmetric(horizontal: 10),
                    icon: Icon(Icons.settings),
                    label: Text('Settings')),
              ],
              indicatorColor: Colors.deepPurple.shade100.withOpacity(0.8),
              indicatorShape: const RoundedRectangleBorder(
                borderRadius: BorderRadius.all(Radius.circular(10)),
              ),
              onDestinationSelected: (value) => setState(() {
                index = value;
              }),
              selectedIndex: index,
            ),
          ),
          Expanded(
            child: Column(
              spacing: 20,
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: [
                // ElevatedButton(
                //   onPressed: () {
                //     // Handle button press
                //   },
                //   child: const Text('Start File Monitoring'),
                // ),
                // ElevatedButton(
                //   onPressed: () {
                //     // Handle button press
                //   },
                //   child: const Text('Start Process Monitoring'),
                // ),
                // ElevatedButton(
                //   onPressed: () {
                //     // Handle button press
                //   },
                //   child: const Text('Start System Monitoring'),
                // ),
                // ElevatedButton(
                //   onPressed: () {
                //     // Handle button press
                //   },
                //   child: const Text('Start Network Monitoring'),
                // ),
                // ElevatedButton(
                //     onPressed: () {}, child: const Text('Live Threat Meter')),
                threatMeter(threatLevel: 'risky'),
                RichText(
                    text: TextSpan(
                  text: 'Monitoring: ',
                  style: const TextStyle(
                      fontSize: 20, fontWeight: FontWeight.bold),
                  children: <TextSpan>[
                    TextSpan(
                      text: isMonitoring ? 'ON' : 'OFF',
                      style: TextStyle(
                          fontSize: 20,
                          color: isMonitoring ? Colors.green : Colors.red,
                          fontWeight: FontWeight.bold),
                    ),
                  ],
                )),
                ElevatedButton(
                    onPressed: () {
                      setState(() {
                        isMonitoring = !isMonitoring;
                      });
                    },
                    child: const Text('Start/Stop Monitoring')),
                FutureBuilder(
                    future: summary,
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return const Center(child: CircularProgressIndicator());
                      } else if (snapshot.hasData) {
                        var monitoring = snapshot.data!['monitoring_summary'];
                        return Column(
                          children: [
                            RichText(
                                text: TextSpan(
                              text: 'Benign: ',
                              style: const TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.bold),
                              children: <TextSpan>[
                                TextSpan(
                                  text: '${monitoring['benign']}',
                                  style: TextStyle(
                                      fontSize: 18,
                                      color: Colors.grey.shade300,
                                      fontWeight: FontWeight.w500),
                                ),
                              ],
                            )),
                            RichText(
                                text: TextSpan(
                              text: 'Malicious: ',
                              style: const TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.bold),
                              children: <TextSpan>[
                                TextSpan(
                                  text: '${monitoring['malicious']}',
                                  style: TextStyle(
                                      fontSize: 18,
                                      color: Colors.grey.shade300,
                                      fontWeight: FontWeight.w500),
                                ),
                              ],
                            )),
                            RichText(
                                text: TextSpan(
                              text: 'Total Events: ',
                              style: const TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.bold),
                              children: <TextSpan>[
                                TextSpan(
                                  text: '${monitoring['total_events']}',
                                  style: TextStyle(
                                      fontSize: 18,
                                      color: Colors.grey.shade300,
                                      fontWeight: FontWeight.w500),
                                ),
                              ],
                            )),
                            RichText(
                                text: TextSpan(
                              text: 'Last Updated: ',
                              style: const TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.bold),
                              children: <TextSpan>[
                                TextSpan(
                                  text: '${monitoring['last_updated']}',
                                  style: TextStyle(
                                      fontSize: 18,
                                      color: Colors.grey.shade300,
                                      fontWeight: FontWeight.w500),
                                ),
                              ],
                            )),
                          ],
                        );
                      } else if (snapshot.hasError) {
                        return const Center(child: Text('Error fetching data'));
                      } else {
                        return const Center(child: Text('No data available'));
                      }
                    }),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Card(
                      elevation: 2,
                      child: Padding(
                        padding: const EdgeInsets.all(30),
                        child: Column(
                          children: [
                            const Icon(
                              Icons.memory_rounded,
                              size: 50,
                            ),
                            const SizedBox(height: 20),
                            Text('32%',
                                style: TextStyle(
                                    fontSize: 17,
                                    color: Colors.blueGrey.shade200,
                                    fontWeight: FontWeight.bold)),
                            const SizedBox(height: 8),
                            const Text('CPU Usage',
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold))
                          ],
                        ),
                      ),
                    ),
                    Card(
                      elevation: 2,
                      child: Padding(
                        padding: const EdgeInsets.all(30),
                        child: Column(
                          children: [
                            const Icon(
                              Icons.speed,
                              size: 50,
                            ),
                            const SizedBox(height: 20),
                            Text('1.4 GB / 8 GB',
                                style: TextStyle(
                                    fontSize: 17,
                                    color: Colors.blueGrey.shade200,
                                    fontWeight: FontWeight.bold)),
                            const SizedBox(height: 8),
                            const Text('Memory Usage',
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold))
                          ],
                        ),
                      ),
                    ),
                  ],
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
