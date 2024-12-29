Notes on changes to forest-light code.

changed 
        # Switch
        ttk::style element create Switch.indicator image \
            [list $I(off-accent) \
                {selected disabled} $I(on-basic) \
                disabled $I(off-basic) \
                {pressed selected} $I(on-accent) \
                {active selected} $I(on-hover) \
                selected $I(on-accent) \
                {pressed !selected} $I(off-accent) \
                active $I(off-hover) \
            ] -width 46 -sticky w

to

        # Switch
        ttk::style element create Switch.indicator image \
            [list $I(off-basic) \
                {selected disabled} $I(on-basic) \
                disabled $I(off-basic) \
                {pressed selected} $I(on-hover) \
                {active selected} $I(on-hover) \
                selected $I(on-accent) \
                {pressed !selected} $I(off-hover) \
                active $I(off-basic) \
            ] -width 46 -sticky w

to copy azure-ttk-theme/theme/light.tcl 