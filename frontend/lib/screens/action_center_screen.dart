import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ActionCenterScreen extends StatefulWidget {
  const ActionCenterScreen({super.key});

  @override
  State<ActionCenterScreen> createState() => _ActionCenterScreenState();
}

class _ActionCenterScreenState extends State<ActionCenterScreen> {
  late Future<List<dynamic>> quarantineList;

  @override
  void initState() {
    super.initState();
    quarantineList = ApiService.getQuarantinedFiles();
  }

  void restoreFile(String filename) async {
    final success = await ApiService.restoreFile(filename);
    if (success) {
      setState(() => quarantineList = ApiService.getQuarantinedFiles());
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content: Text(success ? 'File restored' : 'Failed to restore')),
      );
    }
  }

  void deleteFile(String filename) async {
    final success = await ApiService.deleteFile(filename);
    if (success) {
      setState(() => quarantineList = ApiService.getQuarantinedFiles());
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(success ? 'File deleted' : 'Failed to delete')),
      );
    }
  }

  void rescanFile(String filename) async {
    final success = await ApiService.rescanFile(filename);
    if (success) {
      setState(() => quarantineList = ApiService.getQuarantinedFiles());
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(success ? 'File scanned' : 'Failed to rescan')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Action Center')),
      body: FutureBuilder<List<dynamic>>(
        future: quarantineList,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text("Error loading quarantine data"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("No quarantined files."));
          }

          var files = snapshot.data!;
          return ListView.builder(
            itemCount: files.length,
            itemBuilder: (context, index) {
              var file = files[index];
              return ListTile(
                title: Text(file['filename']),
                // subtitle: Text(
                //     "Reason: ${file['reason'] ?? 'Unknown'}\nTime: ${file['timestamp'] ?? 'N/A'}"),
                subtitle: Text("Detected: ${file['detected_time']}"),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: const Icon(Icons.restore),
                      onPressed: () => restoreFile(file['filename']),
                    ),
                    IconButton(
                      icon: const Icon(Icons.delete_forever),
                      onPressed: () => deleteFile(file['filename']),
                    ),
                    IconButton(
                      icon: const Icon(Icons.replay_rounded),
                      onPressed: () => rescanFile(file['filename']),
                    ),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}
