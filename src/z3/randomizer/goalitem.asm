;--------------------------------------------------------------------------------
; $7F5010 - Scratch Space (Callee Preserved)
;--------------------------------------------------------------------------------
!GOAL_COUNTER = "$7EF418"
!GOAL_DRAW_ADDRESS = "$7EC72A"
;--------------------------------------------------------------------------------
; Draw Goal Item Indicator
DrawGoalIndicator:

    SEP #$20
    LDA.l GoalItemRequirement : BNE + : BRL .done : + ; Star Meter

    LDA.l !GOAL_COUNTER
    JSR HudHexToDec3Digit
    REP #$20

    LDA.l GoalItemIcon : STA !GOAL_DRAW_ADDRESS ; draw star icon

    LDX.b $05 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+2 ; draw 100's digit
    LDX.b $06 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+4 ; draw 10's digit
    LDX.b $07 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+6 ; draw 1's digit

    SEP #$20
    LDA.l GoalItemRequirement : CMP.b #$FF : BEQ .skip

        LDA.l GoalItemRequirement
        JSR HudHexToDec3Digit
        REP #$20
        LDA.w #$2830 : STA !GOAL_DRAW_ADDRESS+8 ; draw slash
        LDX.b $05 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+10 ; draw 100's digit
        LDX.b $06 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+12 ; draw 10's digit
        LDX.b $07 : TXA : ORA.w #$2400 : STA !GOAL_DRAW_ADDRESS+14 ; draw 1's digit
        BRA .done
    .skip
        REP #$20
        LDA.w #$207F ; transparent tile
        STA !GOAL_DRAW_ADDRESS+8
        STA !GOAL_DRAW_ADDRESS+10
        STA !GOAL_DRAW_ADDRESS+12
    .done
;--------------------------------------------------------------------------------
GoalItemGanonCheck:
	LDA $0E20, X : CMP.b #$D6 : BNE .success ; skip if not ganon
		JSL.l CheckGanonVulnerability
		BCS .success

		.fail
		LDA $0D80, X : CMP.b #17 : !BLT .success ; decmial 17 because Acmlm's chart is decimal
		LDA.b #$00
RTL
		.success
		LDA $44 : CMP.b #$80 ; thing we wrote over
RTL
;--------------------------------------------------------------------------------
;Carry clear = ganon invincible
;Carry set = ganon vulnerable
CheckGanonVulnerability:
	LDA InvincibleGanon : BEQ .success
		;#$00 = Off
	+ : CMP #$01 : BEQ .fail
		;#$01 = On
	+ : CMP #$02 : BNE +
		;#$02 = Require All Dungeons
		LDA $7EF374 : AND.b #$07 : CMP #$07 : BNE .fail ; require all pendants
		LDA $7EF37A : AND.b #$7F : CMP #$7F : BNE .fail ; require all crystals
		LDA $7EF3C5 : CMP.b #$03 : !BLT .fail ; require post-aga world state
		LDA $7EF2DB : AND.b #$20 : CMP #$20 : BNE .fail ; require aga2 defeated (pyramid hole open)
		BRA .success
	+ : CMP #$04 : BNE +
		;#$04 = Require Crystals
		JSL CheckEnoughCrystalsForGanon : !BLT .fail ; require specified number of crystals
		BRA .success
	+ : CMP #$03 : BNE +
		;#$03 = Require Crystals and Aga 2
		JSL CheckEnoughCrystalsForGanon : !BLT .fail ; require specified number of crystals
		LDA $7EF2DB : AND.b #$20 : CMP #$20 : BNE .fail ; require aga2 defeated (pyramid hole open)
		BRA .success
	+ : CMP #$05 : BNE +
		;#$05 = Require Goal Items
		LDA.l !GOAL_COUNTER : CMP GoalItemRequirement : !BLT .fail ; require specified number of goal items
		BRA .success
	+ 
.fail : CLC : RTL
.success : SEC : RTL
;--------------------------------------------------------------------------------
GetRequiredCrystalsForTower:
	BEQ + : JSL.l BreakTowerSeal_ExecuteSparkles : + ; thing we wrote over
	LDA.l NumberOfCrystalsRequiredForTower : CMP.b #$00 : BNE + : JML.l Ancilla_BreakTowerSeal_stop_spawning_sparkles : +
	LDA.l NumberOfCrystalsRequiredForTower : CMP.b #$01 : BNE + : JML.l Ancilla_BreakTowerSeal_draw_single_crystal : +
	LDA.l NumberOfCrystalsRequiredForTower : DEC #2 : TAX
JML.l GetRequiredCrystalsForTower_continue
;--------------------------------------------------------------------------------
GetRequiredCrystalsInX:
	LDA.l NumberOfCrystalsRequiredForTower : CMP.b #$00 : BNE +
		TAX
		RTL
	+

	TXA : - : CMP.l NumberOfCrystalsRequiredForTower : !BLT + : !SUB.l NumberOfCrystalsRequiredForTower : BRA - : +

	INC : CMP.l NumberOfCrystalsRequiredForTower : BNE +
		LDA.b #$08
	+ : DEC : TAX
RTL
;--------------------------------------------------------------------------------
CheckEnoughCrystalsForGanon:
	PHX : PHY
	LDA $7EF37A : JSL CountBits ; the comparison is against 1 less
	PLY : PLX
	CMP.l NumberOfCrystalsRequiredForGanon
RTL
;--------------------------------------------------------------------------------
CheckEnoughCrystalsForTower:
	PHX : PHY
	LDA $7EF37A : JSL CountBits ; the comparison is against 1 less
	PLY : PLX
	CMP.l NumberOfCrystalsRequiredForTower
RTL

