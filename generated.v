module generated_circuit (
    input wire A,
    input wire B,
    input wire C,
    output wire F
);

    wire term_0;
    wire term_1;

    buf g0(term_0, C);
    and g1(term_1, A, B);
    or g2(F, term_0, term_1);

endmodule
