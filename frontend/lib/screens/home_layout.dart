import 'package:flutter/material.dart';
import 'package:ransom_saver/screens/home_screen.dart';
import 'package:ransom_saver/screens/threat_activity_screen.dart';
import 'package:ransom_saver/screens/action_center_screen.dart';
import 'package:ransom_saver/screens/settings_screen.dart'; // ✅ Import settings page

class HomeLayout extends StatefulWidget {
  const HomeLayout({super.key});

  @override
  State<HomeLayout> createState() => _HomeLayoutState();
}

class _HomeLayoutState extends State<HomeLayout> {
  int _selectedIndex = 0;
  bool _isRailExtended = false; // Add this state variable

  static final List<Widget> _pages = [
    const HomeScreen(),
    const ThreatActivityScreen(),
    const ActionCenterScreen(),
    const SettingsPage(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _toggleRail() {
    // Add this method
    setState(() {
      _isRailExtended = !_isRailExtended;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            labelType: NavigationRailLabelType.none,
            extended: _isRailExtended,
            leading: Row(
              children: [
                if (_isRailExtended)
                  const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Text('RansomSaver',
                        style: TextStyle(fontWeight: FontWeight.bold)),
                  ),
                IconButton(
                  icon: Icon(_isRailExtended ? Icons.menu_open : Icons.menu),
                  onPressed: _toggleRail,
                ),
              ],
            ),
            elevation: 4,
            minWidth: !_isRailExtended ? 56 : 72,
            minExtendedWidth: 200,
            backgroundColor: Colors.grey[900]?.withAlpha(120),
            indicatorColor: Colors.grey[800],
            indicatorShape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            destinations: const [
              NavigationRailDestination(
                  icon: Icon(Icons.home_filled), label: Text('Home')),
              NavigationRailDestination(
                  icon: Icon(Icons.shield_outlined), label: Text('Threats')),
              NavigationRailDestination(
                  icon: Icon(Icons.security), label: Text('Actions')),
              NavigationRailDestination(
                  icon: Icon(Icons.tune), label: Text('Settings')),
            ],
            selectedIndex: _selectedIndex,
            onDestinationSelected: _onItemTapped,
          ),
          Expanded(child: _pages[_selectedIndex]),
        ],
      ),
      // bottomNavigationBar: BottomNavigationBar(
      //   currentIndex: _selectedIndex,
      //   onTap: _onItemTapped,
      //   type: BottomNavigationBarType.fixed,
      //   selectedItemColor: Theme.of(context).colorScheme.primary,
      //   items: const [
      //     BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
      //     BottomNavigationBarItem(icon: Icon(Icons.warning), label: 'Threats'),
      //     BottomNavigationBarItem(icon: Icon(Icons.security), label: 'Actions'),
      //     BottomNavigationBarItem(
      //         icon: Icon(Icons.settings), label: 'Settings'),
      //   ],
      // ),
    );
  }
}
