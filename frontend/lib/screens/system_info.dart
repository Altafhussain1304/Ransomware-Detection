import 'package:flutter/material.dart';
import 'package:ransom_saver/widgets/threat_meter.dart';

class SystemInfo extends StatefulWidget {
  const SystemInfo({super.key});

  @override
  State<SystemInfo> createState() => _SystemInfoState();
}

class _SystemInfoState extends State<SystemInfo> {
  int index = 0;
  bool drawerOpen = false;
  bool monitoring = false;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: const BackButton(),
        toolbarHeight: 35,
        leadingWidth: 60,
      ),
      body: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
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
          const Expanded(
            child: Column(
              spacing: 20,
              mainAxisAlignment: MainAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  children: [
                    Card(
                      elevation: 2,
                      child: Padding(
                        padding: EdgeInsets.all(50),
                        child: Column(
                          children: [
                            Icon(
                              Icons.memory_rounded,
                              size: 50,
                            ),
                            SizedBox(height: 20),
                            Text('CPU Usage: 32%',
                                style: TextStyle(
                                    fontSize: 15, fontWeight: FontWeight.bold))
                          ],
                        ),
                      ),
                    ),
                    Card(
                      elevation: 2,
                      child: Padding(
                        padding: EdgeInsets.all(50),
                        child: Column(
                          children: [
                            Icon(
                              Icons.speed,
                              size: 50,
                            ),
                            SizedBox(height: 20),
                            Text('Memory Usage: 1.4 GB / 8 GB',
                                style: TextStyle(
                                    fontSize: 15, fontWeight: FontWeight.bold))
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
