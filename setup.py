from setuptools import setup, find_packages

setup(
    name="feng_libs",
    version="0.1",
    keywords=("feng", "jim", "txz", "utils", "libs"),
    description="自己写的轮子",
    long_description="主要用于自己写的一些工具和便于公司开发的库",
    license="jims Licence",
    url="http://wenfengboy.com",
    author="jim",
    author_email="326695231@qq.com",
    packages=find_packages("."),
    include_package_data=True,
    platforms="any",
    install_requires=[],
    requires=[],
    scripts=[],
    package_dir={'': '.'},
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ]
)
