# Uzaki_Converter
This Converter ,Uzaki_Converter, can change the type of sfen into the type of txt that can be "Teacher_Kifu".
This is written in Python. Uzaki means Japanese famous animation "Uzaki chan ha asobitai",in English,"Uzaki want to play". I am not good at English, so I may makes you misunderstand. But You should watch The Animation "Uzaki chan ha asobitai"  
  
このコンバーター、Uzaki_Converterは、sfenのタイプを「Teacher_Kifu」にできるtxtのタイプに変更できます。
これはPythonで書かれています。 宇崎は、日本の有名なアニメ「宇崎ちゃんは遊びたい」を意味し、英語で「宇崎ちゃんは遊びたい」という意味です。 私は英語が苦手なので、誤解されるかもしれません。 でもアニメ「宇崎ちゃんは遊びたい」は必見です  
  
逆輸入翻訳です。  
「宇崎ちゃんは遊びたい」2期が決定したのでぜひ見てください。面白いですよ

## 2020/12/22 大幅更新
詰みまでしっかり教師にできます（たぶんいらない機能）  
mate後もしっかりやってくれるので、終盤教師作れます(笑)  
教師局面のscoreはその局面における指し手の評価値だったらしいので  
評価値については、  
「棋譜にある手を打った場合、相手は評価値xの最善手を指してくるだろう」  
という評価値xを反転させたものにしました。  
またまた言い換えると  
「こちらが手を打った次に相手が打つ最善手の評価値を反転したもの」  
としました。  
この方が棋譜の指し手を高い精度で評価できるからです。  
このやり方だと教師局面の評価値も詰みの100000できっちり終わるようになりました(笑)  
詰みまでエラーなかったのでたぶん大丈夫です。  
  
### 短い棋譜も教師局面にできるNon_Lambda関数を追加!!!
result 0を常に出させるようにしただけです。  
テストしてないので、なんかあったら教えてください。  


# 使い方：
Pythonは自力で！！

1. YaneuraOu氏のAyaneruをダウンロード
https://github.com/yaneurao/Ayane

2. Uzaki_Converterをダウンロード
名前の由来はPythonのエラーがうざいから。
(自分の力不足)

3. Uzaki_Converterの場所にAyaneruのshogiフォルダがあればOK

4. sfenファイルを持ってきて、cmdから実行

# 最近
resultを、sfenの要素数から勝敗判別して正しい値を出すようにしました。  
それと、YaneuraOuのgoコマンドにもdepthを設定することで、1sで50KBくらい(depth 1のとき)書き込むようになりました  
近々、並行処理に対応した「Super_Uzaki_Converter.py」を作りたい！！  

# 反省
並列処理に苦戦して実装できなかった。  
とりあえず、並列実行するためのbatchファイルでも作ればいいか。 
今後も時間を確保する余裕はなさそうなので、更新は未定  
学校の課題があああああぁぁぁぁぁぁ!!    
  


# ブログ
更新頻度：ほとんど更新しないかも…
https://sites.google.com/view/kiwi3shogiblog/%E3%83%9B%E3%83%BC%E3%83%A0?authuser=0
