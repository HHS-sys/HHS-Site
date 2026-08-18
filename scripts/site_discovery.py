from __future__ import annotations


def llms_text(BASE_URL, PHONE_DISPLAY, EMAIL, SERVICES, service_url, INSTAGRAM, FACEBOOK):
    return f"""
    # Hekman Home Services Inc.

    > Husband-and-wife-led renovation, repair and property improvement company based in Westmount and serving homeowners throughout London and nearby communities.

    Canonical website: {BASE_URL}/
    Phone: {PHONE_DISPLAY}
    Email: {EMAIL}

    ## Core services
    {chr(10).join(f'- {item["name"]}: {BASE_URL}{service_url(slug)}' for slug, item in SERVICES.items())}

    ## Service area
    Based in Westmount. Working throughout London and nearby communities—north, south, east and west. This includes Westmount, Sunningdale, Old North, Stoneybrook, Byron, Oakridge, Riverbend, Medway, Hyde Park, Pond Mills, Old South and other London neighbourhoods.

    ## Selected project stories
    - Melrose-area bathroom and lower-level layout: {BASE_URL}/projects/melrose-bathroom-layout/
      The bathroom moved to the other side of an existing wall and was completed with a tiled shower, wall-hung toilet, vanity, lighting and finish work. The connected plan also created a utility room and finished an exercise room with drywall, ceiling work and paint. The public location is limited to the Melrose area, London, Ontario.
    - Hyde Park kitchen renewal: {BASE_URL}/projects/hyde-park-kitchen-renewal/
      Existing cabinets were refaced, a pantry was built, appliances were reconfigured, a dishwasher was added and the counters, sink and backsplash were renewed. This project was completed for under $20,000; that result is not a fixed package or guarantee for another kitchen.
    - Blackfriars leak investigation and restoration: {BASE_URL}/projects/blackfriars-leak-restoration/
      A small leak opening revealed mold, evidence of mice, structural concerns and knob-and-tube wiring. Hekman Home Services identified the visible conditions, coordinated the appropriate remediation team and qualified trades, then managed the rebuild and finish restoration.
    - Medway flooring and storage transformation: {BASE_URL}/projects/medway-flooring-storage/
      Carpet was removed in three rooms. New plank flooring, relocated and new closets, doors, casing and baseboards improved storage and flow. Surfaces were left seamlessly primed for the homeowner's final paint.
    - Westmount porch and entry revitalization: {BASE_URL}/projects/westmount-porch-entry/
      A completed exterior project for an anonymous repeat Westmount customer and neighbour, including porch and entry work, refreshed exterior lines and lighting.
    - Phased Westmount home transformation, ongoing: {BASE_URL}/projects/westmount-1970s-transformation/
      An ongoing project completed around the clients' timing and budget. The confirmed scope includes layout changes, kitchen work, one powder-room renovation, flooring, pot lights, storage, doors, trim and finishing. The kitchen is not complete; a white 2-inch by 10-inch herringbone backsplash to the ceiling is planned.
    - Hilltop whole-home transformation: {BASE_URL}/projects/hilltop-home-transformation/
    - Anonymous London salon moisture investigation and interior restoration: {BASE_URL}/projects/commercial-salon-repair/
      Moisture at the trim was documented before affected wall material was removed. The connected wall and ceiling surfaces were rebuilt and finished, returning the working salon to a bright client-ready result.
    - Pond Mills connected home repairs and flooring: {BASE_URL}/projects/pond-mills-home-repairs/
      When the home had not sold, the homeowner asked Hekman Home Services to take a closer look. The documented interior sequence follows old-floor removal, preparation, plank installation and completed rooms. The confirmed exterior scope included removing a problem weeping pipe, localized grading and downspout work; those exterior items are described but not presented as a photographed sequence.
    - Anonymous London-area multi-unit deck renewal: {BASE_URL}/projects/multi-unit-deck-renewal/
      Weathered connected rear decks were documented before coordinated construction work. Open construction, board fitting and completed deck and guard surfaces are shown without naming the property.
    - Office kitchen renewal, before through completion: {BASE_URL}/projects/kitchen-renewal/
    - Popcorn ceiling transformation: {BASE_URL}/projects/popcorn-ceiling-transformation/
    - Jetted-tub to glass-shower bathroom conversion: {BASE_URL}/projects/glass-block-bathroom-conversion/

    ## Business identity
    Hekman Home Services Inc. is led by Rene and Steph Hekman. The company provides residential renovation and repair work plus commercial maintenance and repairs. It is fully insured and bondable and brings more than 20 years of hands-on experience to its work.

    Official social profiles:
    - Instagram: {INSTAGRAM}
    - Facebook: {FACEBOOK}
    """
