import 'package:flutter/material.dart';
import '../services/api_service.dart';

class LogsScreen extends StatefulWidget {
  const LogsScreen({super.key});

  @override
  State<LogsScreen> createState() => _LogsScreenState();
}

class _LogsScreenState extends State<LogsScreen> {
  late Future<List<dynamic>> logsFuture;

  @override
  void initState() {
    super.initState();
    logsFuture = ApiService.getLogs();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Event Logs')),
      body: FutureBuilder<List<dynamic>>(
        future: logsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return const Center(child: Text('Failed to load logs'));
          }

          final logs = snapshot.data!;
          if (logs.isEmpty) {
            return const Center(child: Text("No logs available"));
          }

          return ListView.builder(
            itemCount: logs.length,
            itemBuilder: (context, index) {
              final log = logs[index];
              return Card(
                elevation: 2,
                margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                child: ListTile(
                  leading: _iconFromCategory(log['category']),
                  title: Text(log['event'] ?? 'No event description'),
                  subtitle: Text(log['timestamp'] ?? 'Unknown time'),
                ),
              );
            },
          );
        },
      ),
    );
  }

  Icon _iconFromCategory(String? category) {
    switch ((category ?? '').toLowerCase()) {
      case 'info':
        return const Icon(Icons.info, color: Colors.blue);
      case 'warning':
        return const Icon(Icons.warning, color: Colors.orange);
      case 'error':
        return const Icon(Icons.error, color: Colors.red);
      default:
        return const Icon(Icons.event_note);
    }
  }
}
