import 'package:flutter/material.dart';

Widget threatMeter({required String threatLevel}) {
  switch (threatLevel) {
    case 'safe':
      return const CircleAvatar(
        radius: 25,
        backgroundColor: Colors.green,
        child: Icon(Icons.check, color: Colors.white),
      );
    case 'unsafe':
      return CircleAvatar(
        radius: 25,
        backgroundColor: Colors.amber.shade700,
        child: const Icon(Icons.warning, color: Colors.white),
      );
    case 'risky':
      return const CircleAvatar(
        radius: 25,
        backgroundColor: Colors.red,
        child: Icon(Icons.error, color: Colors.white),
      );
  }
  return const CircleAvatar(
    radius: 25,
  );
}
