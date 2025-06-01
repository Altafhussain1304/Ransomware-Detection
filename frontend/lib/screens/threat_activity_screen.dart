import 'package:flutter/material.dart';
import 'package:ransom_saver/services/api_service.dart';

class ThreatActivityScreen extends StatefulWidget {
  const ThreatActivityScreen({super.key});

  @override
  State<ThreatActivityScreen> createState() => _ThreatActivityScreenState();
}

class _ThreatActivityScreenState extends State<ThreatActivityScreen> {
  int index = 0;
  bool drawerOpen = false;
  late Future<List<Map<String, dynamic>>> threats;

  String _formatPascalCase(String? text) {
    if (text == null || text.isEmpty) {
      return "";
    }
    return text.replaceAllMapped(
        RegExp(r'(?<=[a-z])[A-Z]'), (match) => ' ${match.group(0)}');
  }

  @override
  void initState() {
    super.initState();
    threats = ApiService.getSimulatedSummary();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Padding(
      padding: const EdgeInsets.all(10),
      child: FutureBuilder<List<Map<String, dynamic>>>(
        future: threats,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text("Error loading threats"));
          } else {
            final items = snapshot.data!;
            return ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                final item = items[index];
                return Card(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),
                  child: ListTile(
                    leading: Icon(
                      item['prediction'] == 'malicious'
                          ? Icons.warning
                          : Icons.check_circle,
                      color: item['prediction'] == 'malicious'
                          ? Colors.red
                          : Colors.green,
                    ),
                    title: Text(_formatPascalCase(item['yara_match'])),
                    subtitle: Text(
                        'File: ${item['name'] ?? "Unknown"}\nTime: ${item['timestamp'] ?? "Unknown"}'),
                  ),
                );
              },
            );
          }
        },
      ),
    ));
  }
}
