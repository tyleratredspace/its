import vcr

test_vcr = vcr.VCR(
    cassette_library_dir="its/tests/fixtures/cassettes", record_mode="once"
)
