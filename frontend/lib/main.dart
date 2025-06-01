import 'package:flutter/material.dart';
import 'package:ransom_saver/app.dart';
import 'package:ransom_saver/screens/home_screen.dart';
import 'package:ransom_saver/screens/threat_activity_screen.dart';

const pages = [HomeScreen(), ThreatActivityScreen()];
void main() {
  runApp(const RansomSaverApp());
}


