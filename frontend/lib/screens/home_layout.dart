import 'package:flutter/material.dart';
import 'package:ransom_saver/main.dart';

class HomeLayout extends StatefulWidget {
  const HomeLayout({super.key});

  @override
  State<HomeLayout> createState() => _HomeLayoutState();
}

class _HomeLayoutState extends State<HomeLayout> {
  int index = 0;
  bool drawerOpen = false;
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
                    icon: Icon(Icons.security),
                    label: Text('Threat Feed')),
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
            child: pages[index],
          ),
        ],
      ),
    );
  }
}
