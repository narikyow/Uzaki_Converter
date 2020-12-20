# Uzaki_Converter
This Converter ,Uzaki_Converter, can change the type of sfen into the type of txt that can be "Teacher_Kifu".
This is written in Python. Uzaki means Japanese famous animation "Uzaki chan ha asobitai",in English,"Uzaki want to play". I am not good at English, so I may makes you misunderstand. But You should watch The Animation "Uzaki chan ha asobitai"

自己紹介はこれくらい。
# 使い方：
Pythonは自力で！！

1. YaneuraOu氏のAyaneruをダウンロード
https://github.com/yaneurao/Ayane

2. Uzaki_Converterをダウンロード
名前の由来はPythonのエラーがうざいから。
(自分の力不足)

3. Uzaki_Converterの場所にAyaneruのshogiフォルダがあればOK

4. sfenファイルを持ってきて、cmdから実行

# 反省
  並列処理に苦戦して実装できなかった。
  とりあえず、並列実行するためのbatchファイルでも作ればいいか。
  今後も時間を確保する余裕はなさそうなので、更新は未定。
  学校の課題があああああぁぁぁぁぁぁ!!
  
  ところで、教師局面のresultが、作ってる間はなにも気づかなかったのですが、
  勝敗をしっかり記録してたことに気づいた（今）ので、
  至急、
  「（局面のlistの要素数-1)%2 が1なら後手勝利（bで-1,wで1）, 0なら先手勝利(bで1,wで-1)」
  という処理を追加して上げ直します

# ブログ
更新頻度：ほとんど更新しないかも…
https://sites.google.com/view/kiwi3shogiblog/%E3%83%9B%E3%83%BC%E3%83%A0?authuser=0
