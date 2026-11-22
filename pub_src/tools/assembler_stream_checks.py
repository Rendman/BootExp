"""Reader exercises for resident block and source-count boundaries."""
from assembler_article_notes import STREAM_SOURCE

def fence(kind,text):return '```'+kind+'\n'+text.rstrip('\n')+'\n```\n\n'

def exercise(number):
 if number==2:
  return ('''## Cross the input-block boundaries

Enter STREAM.BAS. It writes assembly source text; the assembler still makes every executable byte.

'''+fence('basic',STREAM_SOURCE)+fence('dos','GWBASIC STREAM.BAS')+'''Require LONG.ASM READY, then use SYSTEM to return to DOS. The source contains repeated DB statements and a final different value. Its text occupies 7,176 bytes, including BASIC's closing Control-Z. Tokens and CR/LF pairs cross the 1,024-byte input boundaries. Each pass must read through them without losing or repeating a character.

'''+fence('dos','CHECK A02 LONG.ASM RESULT.COM')+'''Require `OK RESULT.COM 01025 bytes` and PASS. VIEW.BAS must show length 1025: the first 1024 bytes are `41` and the final byte is `42`. The final display row contains that one `42`. Inspect this result as data.

Keep the accepted result before trying an error near the end of the same long input:

'''+fence('dos','COPY RESULT.COM HOLD.COM\nGWBASIC STREAM.BAS')+'''At the BASIC prompt replace line 60 with the following line, then RUN and SYSTEM:

'''+fence('basic','60 PRINT #1,"DB 256"')+fence('dos','CHECK A02 LONG.ASM RESULT.COM\nFC /B HOLD.COM RESULT.COM')+'''Require `ERROR 01025 CODE 4` and FAIL, followed by FC reporting no differences. The reader must reach the final statement before its byte-range check rejects the value.

Run GWBASIC STREAM.BAS again and return with SYSTEM. The saved helper still contains DB 66: the trial change was only in BASIC's memory. This leaves LONG.ASM valid for the copy exercise. Keep STREAM.BAS with the workbench sources.

''')
 if number==3:
  return ('''## Flush full blocks and a final partial block

Use the valid LONG.ASM made with STREAM.BAS: 1024 lines containing DB 65, then DB 66. If it is absent, run GWBASIC STREAM.BAS, require LONG.ASM READY and return with SYSTEM. This driver copies the source bytes without interpreting assembly or treating Control-Z as a source ending.

'''+fence('dos','CHECK A03 LONG.ASM RESULT.COM\nFC /B LONG.ASM ASMA.TMP')+'''Require `OK ASMA.TMP 07176 bytes` and PASS, followed by FC reporting no differences. VIEW.BAS must show ASMA.TMP length 7176. Seven full output blocks and an eight-byte tail are required; a missing final flush or a repeated block changes the comparison. Keep this result as data. RESULT.COM is still the saved assembler executable from the construction build.

''')
 if number==8:
  return ('''## Pass the old line-count limit

Reuse STREAM.BAS from the block-reader exercise. Run GWBASIC STREAM.BAS, then replace these two BASIC lines:

'''+fence('basic','10 N=4000\n40 PRINT #1,";"')+'''Leave line 60 as `60 PRINT #1,"DB 66"`. Save this version under its own name, then run it:

'''+fence('basic','SAVE "LINES.BAS",A\nRUN\nSYSTEM')+'''Require LONG.ASM READY before leaving BASIC. The source now has 4000 comment lines and one DB statement: 4001 physical lines with one emitted byte. STREAM.BAS retains the earlier block exercise; LINES.BAS retains these comment-generating lines.

'''+fence('dos','CHECK A08 LONG.ASM RESULT.COM')+'''Require `OK RESULT.COM 00001 bytes` and PASS. VIEW.BAS must show exactly `42`. A07 stops at this source's line 4001 with code 5; A08 must reach the data statement.

## Check the representable limit

Run GWBASIC LINES.BAS. At its prompt set line 10 to `10 N=65534`, RUN, and return to DOS with SYSTEM. This creates 65535 physical lines, including the final DB statement. Run the same CHECK command: require `OK RESULT.COM 00001 bytes` and PASS, with exactly `42` in VIEW.BAS.

Preserve that accepted result with `COPY RESULT.COM HOLD.COM`. Run GWBASIC LINES.BAS again, set line 10 to `10 N=65535`, RUN and return with SYSTEM. There are now 65536 physical lines:

'''+fence('dos','CHECK A08 LONG.ASM RESULT.COM\nFC /B HOLD.COM RESULT.COM')+'''Require `ERROR 65535 CODE 5` and FAIL, followed by FC reporting no differences. The line report remains at 65535 because the counter cannot represent 65536; it must never wrap to zero. Run the saved LINES.BAS again and return with SYSTEM to restore its 4001-line input. Keep these outputs as data.

''')
 return ''
