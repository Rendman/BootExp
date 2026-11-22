"""Checkpoint-specific explanations for the two small assembler collections."""

ASM0_NOTES={
 1:'Check HELLOMSG for the dollar terminator and the explicit carriage-return/line-feed bytes. TEXT returns with RET; GOOD terminates through DOS function 4CH.',
 2:'Check the five divisors and the order of the saved registers in NUMBER. The remainder belongs in CX while DOS prints DL; retaining it in AL would lose it during the DOS call.',
 3:'Save the reason in ERRCODE before TEXT or NUMBER is called. If the normal program reports code 7, check its entry SP requirement; keep the deliberately altered stack test in SMALL.ASM.',
 4:'Check the zero after SOURCE.ASM and save the handle returned in AX only after a successful open. Both open and close must test carry before another instruction changes the flags.',
 5:'Test the returned AX count before using CHAR: a zero count means EOF and leaves no new character to print. Check that the driver closes the source after its reading loop.',
 6:'Check ENDED and SKIPLF, especially the CR/LF pair and the final line without an ending. The 120-character bound applies to the entire physical line, including comments; its zero terminator needs the extra byte.',
 7:'Check that punctuation is returned separately and that a semicolon ends the statement. Save the line cursor SI while ZTEXT displays the token; otherwise scanning resumes in the token buffer.',
 8:'Check the eight-byte record stride and the explicit record count. LOOK must compare both zero terminators; accepting a prefix would confuse a short name with a longer one.',
 9:'Check the decimal overflow comparison before multiplication and the final digit at 6553. VALUE must restore SI so FINISH can inspect the rest of the same statement.',
 10:'Check that the trailing H is excluded from the digit loop and that a hexadecimal token begins with a decimal digit. Decimal and hexadecimal overflow use different pre-multiplication bounds.',
 11:'Keep target PC distinct from resident OUTPTR. EMIT must check capacity before storing, and BYTEVALUE must reject a word above 255 before copying AL. This checkpoint reports a count without writing RESULT.COM.',
 12:'Check that the DOS write count is PC minus 0100H, not PC itself. Test both carry and AX against the requested count, then check the close; an older OK report cannot establish that this write succeeded.',
 13:'Check the counted DB table record and the dispatch class. DATAITEM must require a new value after every comma, including a comma at the end of the line.',
 14:'Check the DW parameter and the two calls to EMIT. The low byte is written first; saving AX across the operation keeps the original high byte available.',
 15:'Check every PASSSTART reset and reopen the input after closing it. Pass one counts and pass two stores; neither pass should append another copy to the output buffer.',
 16:'Check the four-byte register records and the distinction between AL\'s valid code zero and the miss result FFFFH. A recognized register in a data value must take the symbol-error path.',
 17:'Check the first-character rule separately from the remaining name characters. A label must finish its statement after the colon. DEFINE checks spelling here; it does not yet retain definitions.',
 18:'Check the twenty-byte symbol stride and the value at byte offset eighteen. Initialize SYMC and SYMNEXT once, outside PASSSTART, so the first-pass table survives the second pass.',
 19:'Keep both the numeric and symbol error exits. VALUE must restore the source cursor after lookup. A forward reference is provisional only on pass one; pass two must find its definition before output is written.',
 20:'Check each class-two table parameter against the expected opcode. FIXED emits that byte and FINISH rejects an extra operand. These fragments have no prepared stack or index registers for execution.',
 21:'Check K1, W1 and R1 after reading the second operand. The destination width selects B0H or B8H and the immediate width; a byte value must pass BYTEVALUE without truncation.',
 22:'Check SAMEWIDTH before constructing ModR/M. The destination belongs in bits 5–3 and the source in bits 2–0; reload any encoding value changed by the width check.',
 23:'Check that SINGLE accepts only the word-register half of REGTAB and subtracts eight before adding the opcode base. Balance the generated PUSH and POP operations before a return.',
 24:'Save the interrupt value while emitting CDH, then restore it for BYTEVALUE. The runnable test must load AH for each DOS service and finish with AX=4C00H.',
 25:'Check the arithmetic group numbers rather than assigning consecutive table selectors. Register forms and full-width immediate forms use different opcode calculations; CMP emits an operation that changes flags without storing a result.',
 26:'Check the saved first operand V1 for a direct store. Direct addressing requires a word offset after ModR/M; [BX] does not. The ordinary register supplies the memory width.',
 27:'Compute the displacement from PC plus three and retain it while emitting E8H or E9H. For CALL, the called routine must restore its saved words before RET uses the return offset.',
 28:'Compute short reach from PC plus two. Check the signed-byte range on pass two and emit only its low byte. In a runnable loop, the conditional must use the flags from its intended comparison.',
}

ASM1_NOTES={
 1:'Check the six spelling bytes, the table count of twenty-six, class four and selector six. Register widths must agree. The existing arithmetic encoder supplies the instruction bytes.',
 2:'Check RDPOS against RDLEN before refilling. Consume every byte of a short positive read; only a zero read is file EOF. Reset both cursors before each input pass.',
 3:'Check that a full block is flushed before another byte is stored and that the final partial block is flushed before close. FLUSH must preserve the caller\'s byte and counters and verify the actual write count.',
 4:'Set ownership flags only after successful DOS calls. ERROR must save its category before CLEANUP changes AX; cleanup must neither recurse through ERROR nor delete a temporary file owned by another run.',
 5:'Run PREFLIGHT before CREATEOUT. A reserved file is evidence to inspect, not permission to truncate it. Remove only the RECOVERY file deliberately created for this test.',
 6:'Trace HAVEBAK and OWNTMP through each rename. The temporary output must be closed before publication, and a failed replacement must attempt to restore the saved result.',
 7:'Reset the input cursors and PC for each pass. Save ENDPC after pass one, create output only for pass two and compare the final position before flushing and publishing.',
 8:'Check the limit before LINENO wraps from FFFFH to zero. The rejection report stays at 65535 because a 16-bit counter cannot represent the next line.',
 9:'Check every relocated line, token and block-buffer address, along with the twenty-byte symbol stride. The 2048th record ends at EFFFH; the next definition must fail before touching the stack reservation.',
 12:'Use the same unchanged ASM1 source for both self-builds and compare whole files with FC /B. Keep the ASM0-built original separate from RESULT.COM and from both generated copies.',
}

STREAM_SOURCE='''10 N=1024
20 OPEN "LONG.ASM" FOR OUTPUT AS #1
30 FOR I=1 TO N
40 PRINT #1,"DB 65"
50 NEXT I
60 PRINT #1,"DB 66"
70 CLOSE #1
80 PRINT "LONG.ASM READY"
'''
