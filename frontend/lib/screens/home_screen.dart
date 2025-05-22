import 'package:flutter/material.dart';
import 'package:ransom_saver/screens/system_info.dart';
import 'package:ransom_saver/widgets/threat_meter.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int index = 0;
  bool drawerOpen = false;
  bool monitoring = false;
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
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  children: <TextSpan>[
                    TextSpan(
                      text: monitoring ? 'ON' : 'OFF',
                      style: TextStyle(
                          fontSize: 20,
                          color: monitoring ? Colors.green : Colors.red,
                          fontWeight: FontWeight.bold),
                    ),
                  ],
                )),
                ElevatedButton(
                    onPressed: () {
                      setState(() {
                        monitoring = !monitoring;
                      });
                    },
                    child: const Text('Start/Stop Monitoring')),
                ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) => const SystemInfo()));
                    },
                    child: const Text('System Info Section')),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
