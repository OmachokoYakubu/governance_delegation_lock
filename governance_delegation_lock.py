from glider import *

def query():
    """
    @title: Governance Delegation Lock Vulnerability (NounsDAO Style)
    @description: Detects governance contracts where delegation to address(0) locks voting.
                  If delegates(account) returns account when _delegates[account] == 0,
                  tokens become permanently locked from governance participation.
    @author: Hackerdemy Team
    @tags: governance, delegation, voting, lock
    @severity: Epic
    @references: https://mirror.xyz/verbsteam.eth/TP917T6vm6gXuVAxbQ34ZCn7dNiHabu3UW-ninwalVc
    """
    
    # Find functions related to delegation
    delegate_functions = (
        Functions()
        .with_name('delegate')
        .exec(100)
    )
    
    vulnerable = []
    
    for func in delegate_functions:
        source = func.source_code()
        
        # Vulnerable pattern: delegation without address(0) validation
        # If function allows delegating to address(0), tokens can be locked
        has_zero_check = 'address(0)' in source and ('require' in source or 'revert' in source)
        
        if not has_zero_check:
            vulnerable.append(func)
    
    return vulnerable
