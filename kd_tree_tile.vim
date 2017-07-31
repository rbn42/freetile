function! TileFocusWindow(window)

    let curNr = winnr()
    if 'left'==a:window
        wincmd h
    elseif 'down'==a:window
        wincmd j
    elseif 'up'==a:window
        wincmd k
    elseif 'right'==a:window
        wincmd l
    endif

    if winnr() == curNr
        return 0
    else
        return 1
    endif
endfunction

