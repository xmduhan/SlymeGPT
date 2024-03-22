FROM alpine:latest

# 安装 X11 服务器和 LXDE 桌面环境
RUN apk update && \
    apk add --no-cache xorg-server xf86-video-vesa xf86-input-synaptics openbox lxde-common lxsession dbus dbus-x11 ttf-freefont mesa-dri-swrast && \
    rm -rf /var/cache/apk/*

# 设置环境变量
ENV DISPLAY=:0

# 启动 LXDE 桌面环境
CMD startx /usr/bin/lxsession

