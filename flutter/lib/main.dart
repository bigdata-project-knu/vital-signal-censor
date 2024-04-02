import 'package:flutter/material.dart';
import 'package:firstflutter/pages/login_page.dart';
import 'package:firstflutter/style/app_colors.dart';
import 'package:firstflutter/pages/main_page.dart';

void main() {
  runApp(MyApp());}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) { //
    return MaterialApp(
        theme: ThemeData(
          fontFamily: 'NanumGothic',
          scaffoldBackgroundColor: AppColors.background),
        initialRoute: '/',// 초기 경로
        routes: {
          '/': (context) => LoginPage(),
          '/home': (context) => MainPage(),
          '/main': (context) => MainPage(),
    );
  }
}