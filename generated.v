module generated_circuit (
    input wire A,
    input wire B,
    input wire C,
    output wire F
);

    wire not_A;
    wire not_C;
    wire term_0;
    wire term_1;

    not g0(not_A, A);
    not g1(not_C, C);
    and g2(term_0, not_A, B);
    and g3(term_1, A, not_C);
    or g4(F, term_0, term_1);

endmodule
