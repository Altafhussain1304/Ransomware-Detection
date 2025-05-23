import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:ransom_saver/config/api_config.dart';

class ApiService {
  Future<Map<String, dynamic>> getSummary() async {
    final response =
        await http.get(Uri.parse('${ApiConfig.baseUrl}/api/summary'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = await jsonDecode(response.body);
      return data;
    } else {
      throw Exception('Failed to load summary');
    }
  }
}
