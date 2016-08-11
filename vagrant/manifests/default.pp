# puppet manifest

# Make sure the correct directories are in the path:
Exec {
    path => [
    '/usr/local/sbin',
    '/usr/local/bin',
    '/usr/sbin',
    '/usr/bin',
    '/sbin',
    '/bin',
    ],
    logoutput => true,
}

exec {'apt-get-update':
    command => 'apt-get update'
}

package {'build-essential':
    ensure => latest,
    require => Exec['apt-get-update'],
}
package {'python2.7':
    ensure => latest,
    require => Exec['apt-get-update'],
}
package {'python-dev':
    ensure => latest,
    require => Exec['apt-get-update'],
}
package {'python-pip':
    ensure => latest,
    require => Exec['apt-get-update'],
}
package {'git':
    ensure => latest,
    require => Exec['apt-get-update'],
}
package {'nginx':
    ensure => latest,
    require => Exec['apt-get-update'],
}

exec {'upgrade-pip':
	command => 'sudo pip install -U pip',
	require => Package['python-pip']
}
exec {'install-python-requirements':
	cwd => '/vagrant',
	command => 'sudo pip install -r requirements.txt',
	require => Exec['upgrade-pip'],
	user => 'vagrant',
	group => 'vagrant',
	logoutput => true,
}

