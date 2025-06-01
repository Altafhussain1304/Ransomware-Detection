import 'package:flutter/material.dart';
import 'package:ransom_saver/screens/home_layout.dart';
class RansomSaverApp extends StatelessWidget {
  const RansomSaverApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RansomSaver',
      themeMode: ThemeMode.system,
      theme: ThemeData(useMaterial3: true, brightness: Brightness.light),
      darkTheme: ThemeData(useMaterial3: true, brightness: Brightness.dark),
      home: const HomeLayout(),
      debugShowCheckedModeBanner: false,
    );
  }
}
