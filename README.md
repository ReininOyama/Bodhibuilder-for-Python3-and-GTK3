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
簡単にインストールする方法は、
sudo dpkg -i bodhibuilder_3.0.0.deb
とやってから、
sudo apt --fix-broken install
を実行することです。
あ！そうそう！
ubiquityのスライドショーのどれかをインストールしないと、
bodhi のスライドショーになってしまいます。
嫌な人は、
sudo apt install ubiquity-slideshow-ubuntu(ubuntu でなくても xubuntu でもその他でもいい)
とやっておくこと。
/usr/share/ubiquity-slldeshow 以下に独自のスライドショーを入れておくのも可です。
では、お楽しみください。<br>
