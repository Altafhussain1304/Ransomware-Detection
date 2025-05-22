import 'package:http/http.dart' as http;
import 'package:ransom_saver/config/api_config.dart';

class ApiService {
  void fetchSummary() {
    http.get(Uri(path: '${ApiConfig.baseUrl}/api/summary')).then((response) {
      if (response.statusCode == 200) {
        // Handle successful response
      } else {
        // Handle error response
      }
    }).catchError((error) {
      // Handle network error
    });
  }
}
