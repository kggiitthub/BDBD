FROM ubuntu:24.04
# 必要最低限のツールとSSHサーバーのインストール
RUN apt-get update && apt-get install -y \
    openssh-server \
    iproute2 \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# SSHの設定（rootログインの許可とパスワード認証の有効化）
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
# パスワード認証を無効化して鍵認証を推奨（root のパスワードログインは制限）
RUN sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config \
 && sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config || true
RUN sed -i 's/^#\?UsePAM.*/UsePAM yes/' /etc/ssh/sshd_config || true

# コピー: ビルドコンテキストの公開鍵を root の authorized_keys に配置
COPY keys/authorized_keys /root/.ssh/authorized_keys
RUN mkdir -p /root/.ssh \
 && chown root:root /root/.ssh/authorized_keys || true \
 && chmod 700 /root/.ssh || true \
 && chmod 600 /root/.ssh/authorized_keys || true

# SSHポートの開放
EXPOSE 22

# SSHサービスをフォアグラウンドで起動
CMD ["/usr/sbin/sshd", "-D"]
