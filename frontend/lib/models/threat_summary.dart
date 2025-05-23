class ThreatSummary {
  final String? threatLevel;
  final bool? benign;
  final bool? suspicious;
  final bool? malicious;

  ThreatSummary({
    this.threatLevel = '',
    this.benign = false,
    this.suspicious = false,
    this.malicious = false,
  });

  factory ThreatSummary.fromJson(Map<String, dynamic> json) {
    return ThreatSummary(
      threatLevel: json['threat_level'] as String?,
      benign: json['benign'] as bool?,
      suspicious: json['suspicious'] as bool?,
      malicious: json['malicious'] as bool?,
    );
  }
}
