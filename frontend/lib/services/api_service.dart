import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:ransom_saver/config/api_config.dart';

class ApiService {
  static Future<Map<String, dynamic>> getMonitoringSummary() async {
    final response =
        await http.get(Uri.parse('${ApiConfig.baseUrl}/api/summary'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = await jsonDecode(response.body);
      return data['monitoring_summary'];
    } else {
      throw Exception('Failed to load monitoring summary');
    }
  }

  static Future<List<Map<String, dynamic>>> getSimulatedSummary() async {
    final response =
        await http.get(Uri.parse('${ApiConfig.baseUrl}/api/summary'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = await jsonDecode(response.body);
      return List<Map<String, dynamic>>.from(data['simulated_summary']);
    } else {
      throw Exception('Failed to load simulated summary');
    }
  }
}
