---
date: 2026-07-12
tags: []
aliases: []
id: "20260712130351"
---
# iMac 2019 5K 安装 Arch Linux 日志

## 设备与目标

- 设备：iMac 27-inch Retina 5K 2019
- 芯片：Intel + Apple T2
- 显卡：AMD Radeon Pro 5300，Navi 14
- 内存：72 GB
- 硬盘：Apple SSD 512 GB
- 安装方式：整盘安装 Arch Linux，不保留 macOS
- 安装镜像：T2 Linux 官方 `archiso-t2`
- 桌面环境：GNOME + Wayland
- 文件系统：Btrfs + 子卷

---

## 1. 制作启动盘

MacBook Pro M5 使用：

```text
balenaEtcher arm64
```

将 `archiso-t2` ISO 写入 U 盘。

在 iMac 启动时按住：

```text
Option ⌥
```

选择 U 盘的 `EFI Boot`。

---

## 2. 磁盘分区

确认磁盘：

```bash
lsblk -o NAME,SIZE,TYPE,MODEL
```

识别结果：

```text
/dev/sda       U 盘
/dev/nvme0n1   iMac 内置 SSD
```

使用：

```bash
cfdisk /dev/nvme0n1
```

创建：

| 分区 | 大小 | 类型 |
|---|---:|---|
| `/dev/nvme0n1p1` | 1 GiB | EFI System |
| `/dev/nvme0n1p2` | 剩余空间 | Linux filesystem |

写入分区表：

```text
Write → yes → Quit
```

---

## 3. 格式化

EFI：

```bash
mkfs.fat -F32 /dev/nvme0n1p1
```

原 APFS 签名仍存在，需要强制创建 Btrfs：

```bash
mkfs.btrfs -f -L Arch /dev/nvme0n1p2
```

---

## 4. 创建 Btrfs 子卷

```bash
mount /dev/nvme0n1p2 /mnt

btrfs subvolume create /mnt/@
btrfs subvolume create /mnt/@home
btrfs subvolume create /mnt/@var
btrfs subvolume create /mnt/@snapshots

umount /mnt
```

重新挂载：

```bash
mount -o noatime,compress=zstd:3,subvol=@ /dev/nvme0n1p2 /mnt

mkdir -p /mnt/{boot,home,var,.snapshots}

mount -o noatime,compress=zstd:3,subvol=@home \
  /dev/nvme0n1p2 /mnt/home

mount -o noatime,compress=zstd:3,subvol=@var \
  /dev/nvme0n1p2 /mnt/var

mount -o noatime,compress=zstd:3,subvol=@snapshots \
  /dev/nvme0n1p2 /mnt/.snapshots

mount /dev/nvme0n1p1 /mnt/boot
```

检查：

```bash
findmnt -R /mnt
```

---

## 5. 配置代理

中国大陆访问 T2 仓库不稳定，通过 MacBook 的 Clash Verge Rev 共享代理。

MacBook：

- 开启「局域网连接」
- Mixed Port：`7897`
- IP：`192.168.26.7`

Arch Live：

```bash
export http_proxy=http://192.168.26.7:7897
export https_proxy=http://192.168.26.7:7897
```

测试：

```bash
curl -I https://github.com
```

---

## 6. 安装基础系统

第一次 `pacstrap` 因镜像失败，造成 `/var` 子卷不完整。重新挂载后分阶段安装。

核心系统：

```bash
pacstrap -K /mnt \
  base \
  base-devel \
  linux-t2 \
  linux-t2-headers \
  linux-firmware
```

确认：

```bash
ls -ld /mnt/var/lib/pacman
ls /mnt/var
```

生成挂载表：

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

进入系统：

```bash
arch-chroot /mnt
```

---

## 7. 配置 T2 仓库

在 `/etc/pacman.conf` 末尾加入：

```ini
[arch-mact2]
SigLevel = Never
Include = /etc/pacman.d/arch-mact2-mirrorlist
```

同步：

```bash
pacman -Sy
```

安装 T2 相关包：

```bash
pacman -S \
  apple-bcm-firmware \
  apple-t2-audio-config \
  t2fanrd
```

---

## 8. 系统基础配置

时区：

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
```

语言：

```text
en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8
```

生成：

```bash
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

主机名：

```bash
echo "imac-arch" > /etc/hostname
```

`/etc/hosts`：

```text
127.0.0.1 localhost
::1 localhost
127.0.1.1 imac-arch.localdomain imac-arch
```

创建用户：

```bash
passwd

useradd -m -G wheel -s /bin/bash zl
passwd zl
```

启用 `wheel` 组 sudo 权限：

```text
%wheel ALL=(ALL:ALL) ALL
```

---

## 9. 网络

安装并启用 NetworkManager：

```bash
pacman -S networkmanager iwd
systemctl enable NetworkManager
```

---

## 10. 安装 GRUB

```bash
pacman -S grub efibootmgr
```

安装 EFI 引导：

```bash
grub-install \
  --target=x86_64-efi \
  --efi-directory=/boot \
  --bootloader-id=GRUB
```

生成配置：

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

---

## 11. 修复 mkinitcpio 警告

Btrfs 根分区不需要 `fsck` hook。

原配置：

```text
HOOKS=(... filesystems fsck)
```

删除 `fsck`：

```bash
sudo sed -i 's/ fsck)/)/' /etc/mkinitcpio.conf
```

重新生成：

```bash
sudo mkinitcpio -P
```

---

## 12. 修复 AMD 显卡启动卡顿

初始症状：

```text
Loading Linux linux-t2...
Loading initial ramdisk...
```

使用 `nomodeset` 可以快速进入系统，说明问题与 AMDGPU 固件或 KMS 有关。

补装 AMD 图形组件：

```bash
sudo pacman -Syy

sudo pacman -S \
  linux-firmware-amdgpu \
  mesa \
  vulkan-radeon \
  mesa-utils
```

重新生成 initramfs：

```bash
sudo mkinitcpio -P
```

测试不带 `nomodeset` 后，系统能够正常启动。

最终 GRUB 参数恢复为：

```text
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"
```

重新生成配置：

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

最终启动时间：

```text
7.682s
```

---

## 13. 安装 GNOME

安装组合：

```text
GNOME + Wayland + GDM + PipeWire
```

音频 provider 选择：

```text
pipewire-jack
```

字体 provider 选择：

```text
noto-fonts
```

启用图形登录：

```bash
sudo systemctl enable gdm
sudo systemctl set-default graphical.target
sudo reboot
```

成功进入 GNOME 桌面。

---

## 最终状态

- Arch Linux 正常启动
- `linux-t2` 内核运行正常
- GRUB EFI 引导正常
- AMD Radeon Pro 5300 KMS 正常
- 有线网络正常
- GNOME Wayland 正常
- PipeWire 正常
- Btrfs 子卷正常
- 启动时间约 7.7 秒

## 主要踩坑

1. 普通 Arch ISO 不适合 T2 Mac，改用 `archiso-t2`。
2. 删除分区后仍残留 APFS 签名，Btrfs 格式化需要 `-f`。
3. T2 镜像在中国大陆下载不稳定，需要局域网代理。
4. `/var` 使用独立子卷时必须正确挂载后再运行 `pacstrap`。
5. 新系统必须配置 `arch-mact2` 仓库。
6. Btrfs 根分区可移除 `fsck` hook。
7. AMDGPU 固件缺失会造成启动画面长时间停留。
8. `nomodeset` 仅用于临时排障，不能作为最终桌面参数。