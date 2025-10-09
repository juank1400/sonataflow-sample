package com.redhat.developers;

import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.Collections;
import java.util.List;
import java.util.Map;

@Path("/")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ReservationResource {

    @POST
    @Path("/flights")
    public Response reserveFlight() {
        return Response.ok(Collections.singletonMap("message", "Vuelo reservado")).build();
    }

    @POST
    @Path("/hotels")
    public Response reserveHotel() {
        return Response.ok(Collections.singletonMap("message", "Hotel reservado")).build();
    }

    @GET
    @Path("/flights")
    public Response listFlights() {
        List<Map<String, String>> flights = List.of(
                Map.of("flightNumber", "RH123", "from", "LHR", "to", "RDU"),
                Map.of("flightNumber", "QK456", "from", "MAD", "to", "SFO")
        );
        return Response.ok(flights).build();
    }

    @DELETE
    @Path("/flights/{id}")
    public Response cancelFlight(@PathParam("id") String id) {
        return Response.ok(Collections.singletonMap("message", "Vuelo " + id + " cancelado")).build();
    }

    @GET
    @Path("/hotels")
    public Response listHotels() {
        List<Map<String, String>> hotels = List.of(
                Map.of("hotelName", "Red Hat Inn", "location", "Raleigh"),
                Map.of("hotelName", "Quarkus Lodge", "location", "Remote")
        );
        return Response.ok(hotels).build();
    }

    @DELETE
    @Path("/hotels/{id}")
    public Response cancelHotel(@PathParam("id") String id) {
        return Response.ok(Collections.singletonMap("message", "Reserva de hotel " + id + " cancelada")).build();
    }
}