CONTAINER OFlickerTag
{
	NAME OFlickerTag;
    INCLUDE Texpression;
    
    GROUP ID_TAGPROPERTIES
	{
        REAL CLIGHT_STRENGTH {UNIT PERCENT; CUSTOMGUI REALSLIDER; MIN 0; MAX 1000; STEP 1;}
        REAL CLIGHT_SEED {STEP 1;}
        SEPARATOR { }
        REAL CFLICKER_LIGHT {UNIT PERCENT; CUSTOMGUI REALSLIDER; MIN 0; MAX 200; STEP 1;}
        REAL CFLICKER_PROB {UNIT PERCENT; CUSTOMGUI REALSLIDER; MIN 0; MAX 100; STEP 1;}
        LONG CFLICKER_LENGTH {CUSTOMGUI LONGSLIDER; MIN 1; MAX 15; STEP 1;}
        REAL CFLICKER_LENGTH_VAR {UNIT PERCENT; CUSTOMGUI REALSLIDER; MIN 0; MAX 500; STEP 1;}
	}
}