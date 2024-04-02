import 'package:flutter/material.dart';
import 'package:firstflutter/style/app_colors.dart';
// import 'package:flutter/src/widgets/placeholders.dart';
import 'package:flutter/src/widgets/framework.dart';

  class HomePage extends StatelessWidget {
    const HomePage({super.key});

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
          backgroundColor: AppColors.background,
          title: Text('홈'),
          centerTitle: false,
          actions: [
            IconButton(
              icon: Icon(Icons.search),
              onPressed: () {
                print('search 버튼 클릭됨');
              },
            ),
            IconButton(
              icon: Icon(Icons.more_vert),
              onPressed: () {
                print('more 버튼 클릭됨');
              },
            ),
          ],


        ),
        body: Container()
        );
    }
  }

