import setuptools

try:
    import shuup_setup_utils
except ImportError:
    shuup_setup_utils = None


if __name__ == '__main__':
    setuptools.setup(
        name="shuup-mailchimp",
        version="0.7.8",
        description="Shuup Mailchimp Integration",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"shuup.addon": "shuup_mailchimp=shuup_mailchimp"},
        cmdclass=(shuup_setup_utils.COMMANDS if shuup_setup_utils else {}),
        install_requires=[
            'mailchimp3>=3.0.6,<4'
        ],
    )
