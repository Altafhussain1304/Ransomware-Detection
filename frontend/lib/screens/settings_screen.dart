import 'package:flutter/material.dart';
import '../services/api_service.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool loading = true;
  late Future<Map<String, dynamic>> settings;

  @override
  void initState() {
    super.initState();
    settings = ApiService.getSettings();
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
          bool autoQuarantine = data['auto_quarantine'];

          return Column(
            children: [
              SwitchListTile(
                title: const Text("Enable Real-time Monitoring"),
                value: monitoring,
                onChanged: (val) async {
                  await ApiService.updateSetting('monitoring_enabled', val);

                  final settings = await ApiService.getSettings();
                  setState(() {
                    this.settings = Future.value(settings);
                    monitoring = settings['monitoring_enabled'];
                  });
                },
              ),
              SwitchListTile(
                title: const Text("Enable Auto Delete"),
                value: autoDelete,
                onChanged: (val) async {
                  await ApiService.updateSetting('auto_delete', val);
                  final settings = await ApiService.getSettings();
                  setState(() {
                    this.settings = Future.value(settings);
                    autoDelete = settings['auto_delete'];
                  });
                },
              ),
              SwitchListTile(
                title: const Text("Enable Auto Quarantine"),
                value: autoQuarantine,
                onChanged: (val) async {
                  await ApiService.updateSetting('auto_quarantine', val);
                  final settings = await ApiService.getSettings();
                  setState(() {
                    this.settings = Future.value(settings);
                    autoQuarantine = settings['auto_quarantine'];
                  });
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
