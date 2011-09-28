# http://zeta-puppis.com/2007/09/30/an-introduction-to-pyclutter-part-two/

import clutter

RIPPLE_SPEED = 3000 # speed
RIPPLE_W = 8 # width
RIPPLE_G = 2 # gap
RIPPLE_N = 6 # Max amount of ripple circles
RIPPLE_MIND = 150 # Minimum delay between ripples
RIPPLE_MAXD = 2000 # Maximum delay
#define RIPPLE_WX CLUTTER_INT_TO_FIXED(RIPPLE_W)

SCREEN_W = 640
SCREEN_H = 480

"""
static ClutterEffectTemplate *template;

static void
circle_paint_cb (ClutterActor *actor)
{
  ClutterColor fill_color = { 0xff, 0xff, 0xff, 0xff };
  ClutterFixed radius =
    CLUTTER_UNITS_TO_FIXED (clutter_actor_get_widthu (actor))/2;

  fill_color.alpha = clutter_actor_get_opacity (actor);
  cogl_color (&fill_color);
  cogl_path_move_to (radius, radius);
  cogl_path_arc (radius, radius, radius, radius,
                 CLUTTER_ANGLE_FROM_DEG(0),
                 CLUTTER_ANGLE_FROM_DEG(360));
  cogl_path_line_to (radius-RIPPLE_WX/2, radius);
  cogl_path_arc (radius, radius, radius-RIPPLE_WX/2, radius-RIPPLE_WX/2,
                 CLUTTER_ANGLE_FROM_DEG(0),
                 CLUTTER_ANGLE_FROM_DEG(360));
  cogl_path_close ();
  cogl_path_fill ();
}

void
ripple (ClutterActor *stage, gint x, gint y)
{
  const ClutterColor transp = { 0x00, 0x00, 0x00, 0x00 };
  gint i, n;
  
  n = g_random_int_range (1, RIPPLE_N);
  for (i = 0; i < n; i++)
    {
      gint size;
      ClutterActor *actor = clutter_rectangle_new_with_color (&transp);
      
      size = ((RIPPLE_W * 2) * (i + 1)) + (RIPPLE_G * i);
      clutter_actor_set_size (actor, size, size);
      clutter_actor_set_anchor_point_from_gravity (actor,
                                                   CLUTTER_GRAVITY_CENTER);
      clutter_actor_set_position (actor, x, y);
      clutter_actor_set_opacity (actor, 0x80);
      
      g_signal_connect (actor, "paint", G_CALLBACK (circle_paint_cb), NULL);

      clutter_container_add_actor (CLUTTER_CONTAINER (stage), actor);
      
      clutter_effect_scale (template, actor,
                            CLUTTER_STAGE_WIDTH () / RIPPLE_W,
                            CLUTTER_STAGE_WIDTH () / RIPPLE_W,
                            NULL, NULL);
      clutter_effect_fade (template, actor,
                           0x00,
                           (ClutterEffectCompleteFunc)clutter_actor_destroy,
                           NULL);
    }
}

static gboolean
stage_clicked_cb (ClutterActor *stage, ClutterButtonEvent *event)
{
  ripple (stage, event->x, event->y);
  return TRUE;
}


  
  
"""

def ripple():
        alpha = clutter.Alpha(self.timeline, clutter.ramp_func)
        # Sets the Opacity of alpha object we created above. 
        self.behaviour = clutter.BehaviourOpacity(0xdd, 0, alpha)
        # Apply the behaviour and timeline to our Rectangle that was created above
        self.behaviour.apply(self.rect)

#def button_pressed(_

def main2():
    stage = clutter.stage_get_default()
    stage.set_color(clutter.color_parse("red"))
    stage.set_size(SCREEN_W, SCREEN_H)
    stage.show()
    
    template = clutter.EffectTemplate()
    # random_ripple()
      
    stage.connect("key-press-event", clutter.main_quit)
    #stage.connect("key-press-event", clutter.main_quit)
    clutter.main()

def main():
    # A stage is like a gtk.Window
    # By default clutter creates a stage on initializtion, whcih can be retrieved and used as shown below.  It is possilbe that support for multiple stages is present.  If support for multiple stages is present the programmer must manage them using the clutter_actor_destroy function.
    stage = clutter.Stage()
    
    # The size of the stage that is being operated upon is set with the set_size(width, height) function.
    stage.set_size(SCREEN_W, SCREEN_H)
    
    # The color of the stage may be set with the set_color function.  It operates as shown below and takes colors in formats such as #FFFFFF and #FFF.  For the color to be acceptable it must be a clutter color object and is create using cluter.color_parse("TheColor").
    stage.set_color(clutter.color_parse("#BBCCFF"))
    
    
    ## Clutter Rectangles
    # As you are able to see in the code below the same functions are available to different clutter objects such as clutter.Rectangles.  You can use set_size and set_color just as you would on a clutter stage.
    # A word about rectangles are that they are what are called an Actor in clutter.  They are objects that are placed on the stage.
    rect1 = clutter.Rectangle()
    rect2 = clutter.Rectangle()
    
    rect1.set_position(20, 20) # set X and Y coordinates
    rect1.set_size(200, 300)
    rect1.set_color(clutter.color_parse("#A02020"))
    
    rect2.set_position(50, 100)
    rect2.set_size(350, 300)
    rect2.set_color(clutter.color_parse("#00000050"))
    # We can set the border with to what we desire with the set_border_width.  When this is used it obliviously increases the size used in the set_size method.  If the width is 350 now it is 350 + (border *2).  Same goes for the height.
    rect2.set_border_width(20)
    rect2.set_border_color(clutter.color_parse("blue"))
    
    # Very nice part of adding an object to the stage is that you may add as many as you wish using stage.add(object1, object2, etc...)
    stage.add(rect1, rect2)
    
    
    # For you Actors to be shown on the stage you must he stage you must also display all the Actors
    rect1.show()
    rect2.show()
    
    # The stage is shown my using the show() method.
    stage.show()
    
    # Or you may show all the Actors on a stage by using the stages show_all() method.
    stage.show_all()
    stage.connect("key-press-event", clutter.main_quit)
    
    clutter.main()
   
    
if __name__ == "__main__":
    main2()
    
