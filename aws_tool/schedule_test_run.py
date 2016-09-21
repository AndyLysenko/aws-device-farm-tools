import os
from aws_devicefarm_tool import upload_tests, upload_apk, schedule_test_run

project_arn = "arn:aws:devicefarm:us-west-2:825405415122:project:b50019bb-554c-4a9e-8e43-e06875aa5e00"
# app_arn = "arn:aws:devicefarm:us-west-2:825405415122:upload:b50019bb-554c-4a9e-8e43-e06875aa5e00/f3797f10-f745-4f9b-9103-8ba90a4c7660"
app_type = "ANDROID_APP"
test_package_type = "APPIUM_PYTHON_TEST_PACKAGE"
test_run_type = "APPIUM_PYTHON"
# test_package_arn = "arn:aws:devicefarm:us-west-2:825405415122:upload:b50019bb-554c-4a9e-8e43-e06875aa5e00/70dacb80-e31d-46f6-b9df-45b0117fefb2"
device_pool_arn = "arn:aws:devicefarm:us-west-2:825405415122:devicepool:b50019bb-554c-4a9e-8e43-e06875aa5e00/b987ae42-8894-4b40-bdaf-3ca9475dd355"

apk_path = os.path.dirname(os.path.realpath(__file__)) + "/../application/Reader_release_arm7_12536_default_test.apk"
app_name = 'Reader_release_arm7_12536_default_test.apk'

tests_bundle = os.path.dirname(os.path.realpath(__file__)) + "/../test_bundle.zip"
tests_bundle_name = "test_bundle.zip"

run_name = "Test Run 6"

# upload test application
test_app_arn = upload_apk(apk_file=apk_path, project_arn=project_arn, app_name=app_name, app_type=app_type)

# upload test scripts
tests_scripts_arn = upload_tests(test_file=tests_bundle, project_arn=project_arn, file_name=tests_bundle_name,
                                 test_type=test_package_type)

# schedule test run
test_run_arn = schedule_test_run(project_arn=project_arn, app_arn=test_app_arn, device_pool_arn=device_pool_arn,
                                 run_name=run_name, test_type=test_run_type, test_package_arn=tests_scripts_arn)

print "Test run arn= %s" % test_run_arn


