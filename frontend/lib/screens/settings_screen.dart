import 'package:flutter/material.dart';
import '../services/api_service.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool autoDelete = false;
  bool loading = true;
  late Future<Map<String, dynamic>> settings;

  @override
  void initState() {
    super.initState();
    loadSettings();
    settings = ApiService.getSettings();
  }

  void loadSettings() async {
    try {
      final settings = await ApiService.getSettings();
      setState(() {
        autoDelete = settings['auto_delete'] ?? false;
        loading = false;
      });
    } catch (e) {
      setState(() {
        loading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Error loading settings')),
      );
    }
  }

  void toggleAutoDelete(bool value) async {
    setState(() => autoDelete = value);
    try {
      await ApiService.updateSetting('auto_delete', value);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to update setting')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: FutureBuilder(
        future: settings,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text("Failed to load settings"));
          }

          final data = snapshot.data!;
          bool monitoring = data['monitoring_enabled'];
          bool autoDelete = data['auto_delete'];

          return Column(
            children: [
              SwitchListTile(
                title: const Text("Enable Real-time Monitoring"),
                value: monitoring,
                onChanged: (val) {
                  ApiService.updateSetting('monitoring_enabled', val);
                  setState(() => settings = ApiService.getSettings());
                },
              ),
              SwitchListTile(
                title: const Text("Enable Auto Delete"),
                value: autoDelete,
                onChanged: (val) {
                  ApiService.updateSetting('auto_delete', val);
                  setState(() => settings = ApiService.getSettings());
                },
              ),
              const ListTile(
                title: Text("App Version"),
                subtitle: Text("RansomSaver v1.0"),
              ),
              const ListTile(
                title: Text("Developers"),
                subtitle: Text("Built by Azim and Altaf 🚀"),
              )
            ],
          );
        },
      ),
      // body: loading
      //     ? const Center(child: CircularProgressIndicator())
      //     : ListView(
      //         children: [
      //           SwitchListTile(
      //             title: const Text('Auto Delete Threats'),
      //             subtitle: const Text(
      //                 'Automatically delete detected malicious files.'),
      //             value: autoDelete,
      //             onChanged: toggleAutoDelete,
      //           ),
      //           const Divider(),
      //           const ListTile(
      //             title: Text('App Version'),
      //             subtitle: Text('RansomSaver v2.0'),
      //           ),
      //           const ListTile(
      //             title: Text('Developers'),
      //             subtitle: Text('Built by Azim and Altaf 🚀'),
      //           ),
      //         ],
      //       ),
    );
  }
}
