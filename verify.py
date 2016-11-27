import filecmp

def __init__():
    """optional init function that will run when loaded"""
    print "Verifier loaded"

def verify(clean_rc, clean_input_log, clean_output_log, clean_error_log, clean_general_log,
           dirty_rc, dirty_input_log, dirty_output_log, dirty_error_log, dirty_general_log):
        """return False for mismatch, return True for unknown; other posibilities exist, will produce the same effect"""
        rt = aux_verify(clean_rc, clean_input_log, clean_output_log, clean_error_log, clean_general_log,dirty_rc, dirty_input_log, dirty_output_log, dirty_error_log, dirty_general_log)
        if rt:
            print "The automatic verification did not find any indication of failure caused by faults."
            print "This does not mean that the behaviour was correct, or that there are no bugs that can result."
        else:
            print "The automatic verification found mismatch in the logs for the I/O behaviour and/or the return codes"
            print "This means that faults caused failure in the programs."
        return rt


def aux_verify(clean_rc, clean_input_log, clean_output_log, clean_error_log, clean_general_log,
           dirty_rc, dirty_input_log, dirty_output_log, dirty_error_log, dirty_general_log):
        """return False for mismatch, return True for unknown"""
        if clean_rc is None or dirty_rc is None:
            raise Exception
        if clean_rc != dirty_rt:
            return False
        v0 = filecmp.cmp(clean_general_log, dirty_general_log, False)
        v1 = filecmp.cmp(clean_output_log, dirty_output_log, False)
        if not v0 and not v1:
            return False
        v2 = filecmp.cmp(clean_input_log, dirty_input_log, False)
        v3 = filecmp.cmp(clean_error_log, dirty_error_log, False)
        if not v2 and not v3:
            return False
        return True

__init__()