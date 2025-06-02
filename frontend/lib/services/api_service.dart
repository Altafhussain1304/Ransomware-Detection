import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:ransom_saver/config/api_config.dart';

class ApiService {
  static const baseUrl = ApiConfig.baseUrl;
  static Future<Map<String, dynamic>> getMonitoringSummary() async {
    final response = await http.get(Uri.parse('$baseUrl/summary'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = await jsonDecode(response.body);
      final summary = data['monitoring_summary'];
      String threatLevel = 'unknown';
      if (summary['benign'] == 0 && summary['malicious'] == 0) {
        threatLevel = 'safe';
      } else if (summary['benign'] > 0 && summary['malicious'] == 0) {
        threatLevel = 'unsafe';
      } else if (summary['benign'] == 0 && summary['malicious'] > 0) {
        threatLevel = 'risky';
      }
      return {'summary': summary, 'threat_level': threatLevel};
    } else {
      throw Exception('Failed to load monitoring summary');
    }
  }

  static Future<List<Map<String, dynamic>>> getSimulatedSummary() async {
    final response = await http.get(Uri.parse('$baseUrl/summary'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = await jsonDecode(response.body);
      return List<Map<String, dynamic>>.from(data['simulated_summary']);
    } else {
      throw Exception('Failed to load simulated summary');
    }
  }

  static Future<List<dynamic>> getQuarantinedFiles() async {
    final response = await http.get(Uri.parse('$baseUrl/quarantine/list'));

    if (response.statusCode == 200) {
      final data = await json.decode(response.body);
      return data['files'];
    } else {
      throw Exception('Failed to fetch quarantine list');
    }
  }

  static Future<bool> restoreFile(String filename) async {
    final response = await http.post(
      Uri.parse('$baseUrl/quarantine/restore'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'filename': filename}),
    );
    return response.statusCode == 200;
  }

  static Future<bool> deleteFile(String filename) async {
    final response = await http.post(
      Uri.parse('$baseUrl/quarantine/delete'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'filename': filename}),
    );
    return response.statusCode == 200;
  }

  static Future<bool> rescanFile(String fileName) async {
    final response = await http.post(
      Uri.parse('$baseUrl/rescan'),
      body: {'file_name': fileName},
    );
    return response.statusCode == 200;
  }

  static Future<List<dynamic>> getLogs() async {
    final response = await http.get(Uri.parse('$baseUrl/api/logs'));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load logs');
    }
  }

  static Future<Map<String, dynamic>> getSettings() async {
    final response = await http.get(Uri.parse('$baseUrl/settings'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load settings');
    }
  }

  static Future<bool> updateSetting(String key, dynamic value) async {
    final response = await http.put(
      Uri.parse('$baseUrl/settings'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({key: value}),
    );
    return response.statusCode == 200;
  }
}
