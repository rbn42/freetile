pkgname=freetile-git
pkgver=0.1.0
pkgrel=1
pkgdesc="X"
arch=('any')
url="http://github.com/rbn42/freetile"
license=('MIT')
depends=('python-docopt' 'python-xlib' 'python-xcffib' 'python-ewmh' 'python-setproctitle') 
makedepends=('git' 'python-wheel')
provides=('freetile')
conflicts=('freetile')
source=("git+https://github.com/rbn42/freetile")
md5sums=('SKIP')

pkgver() {
  cd "$srcdir/$pkgname"
  git describe --always | sed -e 's|-|.|g' -e '1s|^.||'
}

package() {
  cd "$srcdir/$pkgname"
  # pip install direct from source results slow behavior.
  # see https://github.com/JonathonReinhart/scuba/issues/71#issuecomment-238057064
  python setup.py bdist_wheel
  pip install --compile --no-deps --ignore-installed --root="$pkgdir" dist/${pkgname%-*}-*.whl
  install -Dm644 LICENSE $pkgdir/usr/share/licenses/${pkgname%-*}/LICENSE
}

