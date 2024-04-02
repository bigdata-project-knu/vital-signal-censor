import 'package:flutter/material.dart';
import 'package:firstflutter/pages/home_page.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState(); // 상태 클래스를 반환
}

class _MainPageState extends State<MainPage> {
  Menus currentIndex = Menus.home; // 현재 선택된 메뉴

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('바텀 네비게이션 바')),
      body: pages[currentIndex.index],
      bottomNavigationBar: BottomNavigationBar(
        items: [
          BottomNavigationBarItem(
              icon: Icon(Icons.search), label: '검색'),
          BottomNavigationBarItem(
              icon: Icon(Icons.person), label: '내정보'),
          BottomNavigationBarItem(icon: Icon(Icons.home), label: '홈'),
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: '좋아요'),
          BottomNavigationBarItem(
              icon: Icon(Icons.settings), label: '설정'),
        ],
        onTap: (index) {
          setState(() {
            currentIndex = index;
          });
        },
        showSelectedLabels: false,
        showUnselectedLabels: false,
        selectedItemColor: Colors.amber,
        unselectedItemColor: Colors.grey,
        backgroundColor: Colors.white,
      ),
    );
  }
}

final pages = [
  HomePage(),
  HomePage(),
  HomePage(),
  HomePage(),
HomePage()]


enum Menus { search, profile, home, favorite, setting }

class MyBottomNavigationBar extends StatelessWidget {
  final Menus currentIndex; // 현재 선택된 메뉴
  final ValueChanged<Menus> OnTap;
  const MyBottomNavigationBar({super.key}, required this.currentIndex, required this.onTap);// 생성자

  @override
  Widget build(BuildContext context) {
   return Container(
     height:
   )

