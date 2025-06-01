import 'package:flutter/material.dart';
import '../services/api_service.dart';

class QuarantineScreen extends StatefulWidget {
  const QuarantineScreen({super.key});

  @override
  State<QuarantineScreen> createState() => _QuarantinePageState();
}

class _QuarantinePageState extends State<QuarantineScreen> {
  late Future<List<dynamic>> quarantineList;

  @override
  void initState() {
    super.initState();
    quarantineList = ApiService.getQuarantinedFiles();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Quarantine')),
      body: FutureBuilder<List<dynamic>>(
        future: quarantineList,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error loading quarantine data'));
          } else {
            final data = snapshot.data!;
            if (data.isEmpty) {
              return Center(child: Text("No files in quarantine"));
            }
            if (data == null || data.isEmpty) {
              return const Center(child: Text("No files in quarantine."));
            }
            return ListView.builder(
              itemCount: data.length,
              itemBuilder: (context, index) {
                var file = data[index];

                return Card(
                  elevation: 3,
                  margin: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ListTile(
                          contentPadding: EdgeInsets.zero,
                          leading:
                              Icon(Icons.warning_rounded, color: Colors.red),
                          title: Text(file['filename']),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Path: ${file['filepath']}'),
                              Text('Detected By: ${file['detection_method']}'),
                              Text('Quarantined At: ${file['quarantined_at']}'),
                            ],
                          ),
                          trailing: Text(
                            '${(file['confidence_score'] * 100).toStringAsFixed(1)}%',
                            style: TextStyle(
                              color: Colors.deepOrange,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          isThreeLine: true,
                        ),
                        SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            ElevatedButton(
                              onPressed: () async {
                                bool success = await ApiService.restoreFile(
                                    file['filename']);
                                if (success) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(content: Text('Restored')),
                                  );
                                  setState(() {
                                    quarantineList =
                                        ApiService.getQuarantinedFiles();
                                  });
                                }
                              },
                              child: Text('Restore'),
                            ),
                            SizedBox(width: 10),
                            ElevatedButton(
                              onPressed: () async {
                                bool success = await ApiService.deleteFile(
                                    file['filename']);
                                if (success) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(content: Text('Deleted')),
                                  );
                                  setState(() {
                                    quarantineList =
                                        ApiService.getQuarantinedFiles();
                                  });
                                }
                              },
                              child: Text('Delete'),
                              style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.red),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }
}
