/**
 * generated by Xtext 2.37.0
 */
package com.ensias.dsl.microserviceDSL.tests;

import com.ensias.dsl.microserviceDSL.Gateway;
import com.ensias.dsl.microserviceDSL.MicroserviceDSLFactory;

import junit.framework.TestCase;

import junit.textui.TestRunner;

/**
 * <!-- begin-user-doc -->
 * A test case for the model object '<em><b>Gateway</b></em>'.
 * <!-- end-user-doc -->
 * @generated
 */
public class GatewayTest extends TestCase {

	/**
	 * The fixture for this Gateway test case.
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @generated
	 */
	protected Gateway fixture = null;

	/**
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @generated
	 */
	public static void main(String[] args) {
		TestRunner.run(GatewayTest.class);
	}

	/**
	 * Constructs a new Gateway test case with the given name.
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @generated
	 */
	public GatewayTest(String name) {
		super(name);
	}

	/**
	 * Sets the fixture for this Gateway test case.
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @generated
	 */
	protected void setFixture(Gateway fixture) {
		this.fixture = fixture;
	}

	/**
	 * Returns the fixture for this Gateway test case.
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @generated
	 */
	protected Gateway getFixture() {
		return fixture;
	}

	/**
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @see junit.framework.TestCase#setUp()
	 * @generated
	 */
	@Override
	protected void setUp() throws Exception {
		setFixture(MicroserviceDSLFactory.eINSTANCE.createGateway());
	}

	/**
	 * <!-- begin-user-doc -->
	 * <!-- end-user-doc -->
	 * @see junit.framework.TestCase#tearDown()
	 * @generated
	 */
	@Override
	protected void tearDown() throws Exception {
		setFixture(null);
	}

} //GatewayTest
