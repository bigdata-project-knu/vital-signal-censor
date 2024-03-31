import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) { //
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.white,
        body: Column(
          children: [
            SizedBox(height: 40,),
            Text('어서오세요!'),
            Text('계속할려면 로그인 해주세요'),
            TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                labelText: '아이디',
                hintText: '아이디를 입력해주세요')),
            SizedBox(height: 20),
            TextField(
              decoration: InputDecoration(
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),
                hintText: '비밀번호를 입력해주세요',
                labelText: ' 비밀번호'),
            ),
            Align(
              alignment: Alignment.centerRight,
            child : TextButton(onPressed: (){
              print('forgot 버튼 클릭됨');
            }, child: Text('패스워드를 잊으셨나요?'))),
            TextButton(onPressed: (){
              print('로그인 버튼 클릭됨');
            },
                child: Text('로그인')),
            Text('sign up with'),
            SizedBox(height: 10),
            TextButton(onPressed: (){},
                style: TextButton.styleFrom(
                  backgroundColor: Colors.blue.withOpacity(0.4),
                  foregroundColor: Colors.white,
                ),
                child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/images/google3.png',
                  width: 30,
                  height: 30),
                Text('구글로 로그인'),
                ],
            )),
            SizedBox(height: 15),
            TextButton(onPressed: (){},
            style: TextButton.styleFrom(
            backgroundColor: Colors.blue.withOpacity(0.4),
            foregroundColor: Colors.white,
            ),
            child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
            Image.asset(
            'assets/images/google3.png',
            width: 30,
            height: 30),
            Text('카카오로 로그인'),
            ]
            )),
          ], // Column children

      ),
    );
  }
}


