# Bodhibuilder-for-Python3-and-GTK3<br>
Bodhibuilder 3.0.0 based Python3 and Gobject GTK3 for  Ubuntu 24.04 series.<br>
<br>
Bodhibuilder を、Python3, Gobject GTK3 ベースに改良しました。<br>
これで、Ubuntu 24.04系に 普通にインストールして動作させる事ができます。<br>
まだ、改良の余地があり、起動に少し時間がかかっています。<br>
また、Dist メニューで　インストール用の iso を作製する機能以外は、<br>
動作チェックをしていません。<br>
<br>
でも、それだけでも十分使えると思います。<br>
<br>
１つアドバイスです。<br>
/etc/skel に .config .local などを複製すると、<br>
カスタマイズしたデスクトップ環境が、多くの場合そのままデフォルトで反映されます。<br>
これで、自分で作ったカスタム Ubuntu をインストールしただけで簡単に実現できます。<br>
<br>
簡単にインストールする方法は、<br>
sudo dpkg -i bodhibuilder_3.0.3.deb<br>
とやってから、<br>
sudo apt --fix-broken install<br>
を実行することです。<br>
あ！そうそう！<br>
ubiquityのスライドショーのどれかをインストールしないと、<br>
bodhi のスライドショーになってしまいます。<br>
嫌な人は、<br>
sudo apt install ubiquity-slideshow-ubuntu(ubuntu でなくても xubuntu でもその他でもいい)<br>
とやっておくこと。<br>
/usr/share/ubiquity-slldeshow 以下に独自のスライドショーを入れておくのも可です。<br>
では、お楽しみください。<br>
<br>
テスト環境では正常なのに 新規環境に dpkg でインストールすると動作しなかった。<br>
<br>
原因は、Ubuntuのパッケージ管理のバグの様だ。<br>
ubiquity-frontend-gtkは、前提ソフトなのですが、<br>
前提条件に含めてパッケージを作製すると<br>
何故か、あらぬタイミングで自分自身を消去してしまいます。<br>
仕方ないので、前提から外しました。<br>
sudo apt install ubiquity-frontend-gtk<br>
は、最初に別途実行してからインストールを進めてください。<br>
何と奇っ怪な現象があるものですね。<br>
<br>
バージョン 3.0.3 最初に開くのが遅い問題を解消したはず。<br>
